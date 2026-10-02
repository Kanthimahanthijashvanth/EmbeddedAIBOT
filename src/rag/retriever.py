
import re


class WorkshopRetriever:

    def __init__(
        self,
        vector_store,
        k=5,
        candidate_k=20
    ):
        self.vector_store = vector_store
        self.k = k
        self.candidate_k = candidate_k

    def retrieve(self, query):

        if not query or not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        # -----------------------------------------
        # 1. Semantic retrieval
        # -----------------------------------------

        candidates = self.vector_store.similarity_search(
            query,
            k=self.candidate_k
        )

        # -----------------------------------------
        # 2. Remove duplicate content/source
        # -----------------------------------------

        candidates = self._filter_duplicates(
            candidates
        )

        # -----------------------------------------
        # 3. Keyword-aware reranking
        # -----------------------------------------

        ranked = self._rerank(
            query,
            candidates
        )

        return ranked[:self.k]

    def retrieve_with_scores(self, query):

        if not query or not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        candidates = (
            self.vector_store
            .similarity_search_with_score(
                query,
                k=self.candidate_k
            )
        )

        documents = [
            item[0]
            for item in candidates
        ]

        documents = self._filter_duplicates(
            documents
        )

        ranked = self._rerank(
            query,
            documents
        )

        score_map = {
            id(document): score
            for document, score in candidates
        }

        return [
            (
                document,
                score_map.get(id(document))
            )
            for document in ranked[:self.k]
        ]

    # =====================================================
    # DUPLICATE FILTERING
    # =====================================================

    def _filter_duplicates(self, documents):

        results = []

        seen_content = set()
        seen_sources = set()

        for document in documents:

            content = document.page_content.strip()

            if not content:
                continue

            # Normalize content
            normalized_content = " ".join(
                content.split()
            ).lower()

            # -----------------------------------------
            # Duplicate content
            # -----------------------------------------

            if normalized_content in seen_content:
                continue

            metadata = document.metadata

            file_name = metadata.get(
                "file_name",
                "Unknown"
            )

            slide_number = metadata.get(
                "slide_number"
            )

            page_number = metadata.get(
                "page_number"
            )

            location = (
                slide_number
                if slide_number is not None
                else page_number
            )

            source_key = (
                file_name,
                location
            )

            # -----------------------------------------
            # Duplicate source location
            # -----------------------------------------

            if source_key in seen_sources:
                continue

            seen_content.add(
                normalized_content
            )

            seen_sources.add(
                source_key
            )

            results.append(document)

        return results

    # =====================================================
    # KEYWORD-AWARE RERANKING
    # =====================================================

    def _rerank(self, query, documents):

        query_terms = self._extract_terms(
            query
        )

        query_phrase = self._normalize(
            query
        )

        scored_documents = []

        for document in documents:

            content = self._normalize(
                document.page_content
            )

            metadata = document.metadata

            # -----------------------------------------
            # Content score
            # -----------------------------------------

            content_score = 0

            # Exact phrase
            if query_phrase and query_phrase in content:
                content_score += 10

            # Individual query terms
            for term in query_terms:

                if term in content:
                    content_score += 3

            # -----------------------------------------
            # Metadata score
            # -----------------------------------------

            metadata_text = " ".join([
                str(metadata.get("file_name", "")),
                str(metadata.get("content_type", "")),
            ])

            metadata_text = self._normalize(
                metadata_text
            )

            metadata_score = 0

            for term in query_terms:

                if term in metadata_text:
                    metadata_score += 2

            # -----------------------------------------
            # Technical phrase matching
            # -----------------------------------------

            phrase_score = self._technical_phrase_score(
                query,
                content
            )

            total_score = (
                content_score
                + metadata_score
                + phrase_score
            )

            scored_documents.append(
                (
                    total_score,
                    document
                )
            )

        # Stable sort:
        # documents with higher keyword score first
        scored_documents.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            document
            for score, document in scored_documents
        ]

    # =====================================================
    # TERM EXTRACTION
    # =====================================================

    def _extract_terms(self, text):

        text = text.lower()

        words = re.findall(
            r"\b[a-zA-Z0-9_]+\b",
            text
        )

        # Common question words should not influence ranking
        stop_words = {
            "what",
            "is",
            "are",
            "was",
            "were",
            "the",
            "a",
            "an",
            "of",
            "to",
            "for",
            "in",
            "on",
            "and",
            "or",
            "how",
            "why",
            "when",
            "where",
            "which",
            "explain",
            "describe",
            "tell",
            "me",
            "about",
            "does",
            "do",
            "can",
            "could",
            "would",
            "please"
        }

        terms = [
            word
            for word in words
            if word not in stop_words
        ]

        return list(dict.fromkeys(terms))

    # =====================================================
    # TECHNICAL PHRASE MATCHING
    # =====================================================

    def _technical_phrase_score(
        self,
        query,
        content
    ):

        query = self._normalize(query)

        score = 0

        # Important multi-word technical concepts
        technical_phrases = [
            "stepper motor",
            "servo motor",
            "firmware architecture",
            "hardware abstraction layer",
            "embedded systems",
            "embedded firmware",
            "real time",
            "real time operating system",
            "device driver",
            "peripheral driver",
            "motor control",
            "static testing",
            "dynamic testing",
            "unit testing",
            "integration testing",
            "software testing",
            "machine learning",
            "deep learning",
            "computer networks",
            "interrupt service routine",
            "pulse width modulation",
            "serial peripheral interface",
            "inter integrated circuit",
            "universal asynchronous receiver transmitter",
            "analog to digital converter",
            "digital to analog converter",
            "bootloader",
            "bsp",
            "hal"
        ]

        for phrase in technical_phrases:

            if phrase in query:

                if phrase in content:
                    score += 8

                # If query explicitly asks about
                # a technical phrase, absence of
                # that phrase should not receive
                # the bonus.
                else:
                    score += 0

        return score

    # =====================================================
    # TEXT NORMALIZATION
    # =====================================================

    def _normalize(self, text):

        text = str(text).lower()

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # =====================================================
    # SUMMARY
    # =====================================================

    def get_retrieval_summary(
        self,
        documents
    ):

        summary = []

        for document in documents:

            metadata = document.metadata

            summary.append({
                "content": document.page_content,
                "slide_number": metadata.get(
                    "slide_number"
                ),
                "page_number": metadata.get(
                    "page_number"
                ),
                "file_name": metadata.get(
                    "file_name"
                ),
                "content_type": metadata.get(
                    "content_type"
                ),
                "chunk_id": metadata.get(
                    "chunk_id"
                )
            })

        return summary

