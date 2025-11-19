"""
Text Analysis Service for semantic matching and NLP-based analysis.
Provides text similarity, keyword extraction, and semantic understanding.
"""

from typing import List, Dict, Set, Tuple
import re
from collections import Counter
from dataclasses import dataclass


@dataclass
class TextAnalysisResult:
    """Result of text analysis."""
    similarity_score: float  # 0-100
    matching_keywords: List[str]
    missing_keywords: List[str]
    sentiment_score: float  # 0-100 (positive sentiment)
    readability_score: float  # 0-100
    key_phrases: List[str]


@dataclass
class SkillExtraction:
    """Extracted skills from text."""
    technical_skills: Set[str]
    soft_skills: Set[str]
    tools: Set[str]
    frameworks: Set[str]
    methodologies: Set[str]


class TextAnalysisService:
    """Service for text analysis and semantic matching."""

    # Comprehensive skill taxonomy
    TECHNICAL_SKILLS = {
        # Programming languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
        'php', 'ruby', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl',
        # Web technologies
        'html', 'css', 'sass', 'less', 'webpack', 'babel', 'vite',
        # Databases
        'sql', 'nosql', 'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
        'cassandra', 'dynamodb', 'oracle', 'mssql',
        # Cloud & DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab-ci',
        'terraform', 'ansible', 'chef', 'puppet',
        # Data & ML
        'machine learning', 'deep learning', 'neural networks', 'data science',
        'data analysis', 'statistics', 'pandas', 'numpy', 'scikit-learn',
        'tensorflow', 'pytorch', 'keras',
        # Mobile
        'android', 'ios', 'react native', 'flutter', 'xamarin',
        # Other
        'blockchain', 'iot', 'embedded systems', 'security', 'cryptography',
    }

    SOFT_SKILLS = {
        'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
        'time management', 'adaptability', 'creativity', 'collaboration', 'mentoring',
        'presentation', 'negotiation', 'conflict resolution', 'decision making',
        'emotional intelligence', 'self-motivation', 'attention to detail',
    }

    FRAMEWORKS = {
        'react', 'angular', 'vue', 'svelte', 'next.js', 'nuxt', 'gatsby',
        'django', 'flask', 'fastapi', 'express', 'nest.js', 'spring', 'spring boot',
        '.net', 'asp.net', 'rails', 'laravel', 'symfony',
    }

    METHODOLOGIES = {
        'agile', 'scrum', 'kanban', 'lean', 'waterfall', 'devops', 'ci/cd',
        'tdd', 'bdd', 'pair programming', 'code review', 'continuous integration',
        'continuous deployment', 'microservices', 'monolithic', 'serverless',
    }

    TOOLS = {
        'git', 'github', 'gitlab', 'bitbucket', 'jira', 'confluence', 'slack',
        'trello', 'asana', 'notion', 'figma', 'sketch', 'adobe xd', 'postman',
        'swagger', 'grafana', 'prometheus', 'datadog', 'new relic',
    }

    # Synonyms and related terms
    SKILL_SYNONYMS = {
        'js': 'javascript',
        'ts': 'typescript',
        'k8s': 'kubernetes',
        'ml': 'machine learning',
        'ai': 'artificial intelligence',
        'dl': 'deep learning',
        'rn': 'react native',
        'node': 'node.js',
        'postgres': 'postgresql',
        'mongo': 'mongodb',
        'eks': 'kubernetes',
        'ecs': 'docker',
    }

    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for analysis."""
        if not text:
            return ""
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep letters, numbers, spaces, and common punctuation
        text = re.sub(r'[^a-z0-9\s\.\,\-\+\#]', '', text)
        return text.strip()

    @staticmethod
    def extract_keywords(text: str, min_length: int = 3, top_n: int = 20) -> List[str]:
        """Extract important keywords from text."""
        if not text:
            return []

        normalized = TextAnalysisService.normalize_text(text)

        # Split into words
        words = normalized.split()

        # Filter out common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        }

        # Filter and count
        filtered_words = [w for w in words if len(w) >= min_length and w not in stop_words]
        word_counts = Counter(filtered_words)

        # Get top N most common
        return [word for word, count in word_counts.most_common(top_n)]

    @staticmethod
    def extract_skills(text: str) -> SkillExtraction:
        """Extract skills from text using taxonomy."""
        if not text:
            return SkillExtraction(set(), set(), set(), set(), set())

        normalized = TextAnalysisService.normalize_text(text)

        # Apply synonyms
        for synonym, canonical in TextAnalysisService.SKILL_SYNONYMS.items():
            normalized = re.sub(r'\b' + synonym + r'\b', canonical, normalized)

        # Extract each category
        technical = set()
        for skill in TextAnalysisService.TECHNICAL_SKILLS:
            if re.search(r'\b' + re.escape(skill) + r'\b', normalized):
                technical.add(skill)

        soft = set()
        for skill in TextAnalysisService.SOFT_SKILLS:
            if re.search(r'\b' + re.escape(skill) + r'\b', normalized):
                soft.add(skill)

        frameworks = set()
        for fw in TextAnalysisService.FRAMEWORKS:
            if re.search(r'\b' + re.escape(fw) + r'\b', normalized):
                frameworks.add(fw)

        methodologies = set()
        for method in TextAnalysisService.METHODOLOGIES:
            if re.search(r'\b' + re.escape(method) + r'\b', normalized):
                methodologies.add(method)

        tools = set()
        for tool in TextAnalysisService.TOOLS:
            if re.search(r'\b' + re.escape(tool) + r'\b', normalized):
                tools.add(tool)

        return SkillExtraction(
            technical_skills=technical,
            soft_skills=soft,
            tools=tools,
            frameworks=frameworks,
            methodologies=methodologies,
        )

    @staticmethod
    def calculate_text_similarity(text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts using Jaccard similarity.
        Returns score from 0 to 100.
        """
        if not text1 or not text2:
            return 0.0

        # Extract keywords from both texts
        keywords1 = set(TextAnalysisService.extract_keywords(text1, top_n=50))
        keywords2 = set(TextAnalysisService.extract_keywords(text2, top_n=50))

        if not keywords1 or not keywords2:
            return 0.0

        # Calculate Jaccard similarity
        intersection = len(keywords1.intersection(keywords2))
        union = len(keywords1.union(keywords2))

        if union == 0:
            return 0.0

        similarity = (intersection / union) * 100
        return round(similarity, 2)

    @staticmethod
    def analyze_text_match(
        candidate_text: str,
        vacancy_text: str,
        required_keywords: List[str] = None
    ) -> TextAnalysisResult:
        """
        Comprehensive text analysis comparing candidate and vacancy texts.
        """
        if not candidate_text or not vacancy_text:
            return TextAnalysisResult(
                similarity_score=0.0,
                matching_keywords=[],
                missing_keywords=required_keywords or [],
                sentiment_score=50.0,
                readability_score=50.0,
                key_phrases=[],
            )

        # Calculate similarity
        similarity = TextAnalysisService.calculate_text_similarity(
            candidate_text, vacancy_text
        )

        # Extract keywords from both
        cand_keywords = set(TextAnalysisService.extract_keywords(candidate_text, top_n=30))
        vac_keywords = set(TextAnalysisService.extract_keywords(vacancy_text, top_n=30))

        # Find matches and missing
        matching = list(cand_keywords.intersection(vac_keywords))

        # Check required keywords if provided
        missing = []
        if required_keywords:
            cand_keywords_lower = {k.lower() for k in cand_keywords}
            for req in required_keywords:
                if req.lower() not in cand_keywords_lower:
                    missing.append(req)

        # Simple sentiment analysis (placeholder)
        sentiment = TextAnalysisService._simple_sentiment_analysis(candidate_text)

        # Readability score (placeholder)
        readability = TextAnalysisService._calculate_readability(candidate_text)

        # Extract key phrases
        key_phrases = TextAnalysisService._extract_key_phrases(candidate_text)

        return TextAnalysisResult(
            similarity_score=similarity,
            matching_keywords=matching,
            missing_keywords=missing,
            sentiment_score=sentiment,
            readability_score=readability,
            key_phrases=key_phrases,
        )

    @staticmethod
    def _simple_sentiment_analysis(text: str) -> float:
        """
        Simple sentiment analysis based on positive/negative words.
        Returns score from 0 (negative) to 100 (positive).
        """
        positive_words = {
            'excellent', 'great', 'good', 'best', 'strong', 'skilled', 'experienced',
            'expert', 'proficient', 'successful', 'achieved', 'improved', 'optimized',
            'innovative', 'creative', 'passionate', 'dedicated', 'motivated',
        }

        negative_words = {
            'poor', 'weak', 'limited', 'lacking', 'insufficient', 'failed',
            'struggled', 'difficult', 'problem', 'issue', 'challenge',
        }

        normalized = TextAnalysisService.normalize_text(text)
        words = normalized.split()

        positive_count = sum(1 for w in words if w in positive_words)
        negative_count = sum(1 for w in words if w in negative_words)

        total = positive_count + negative_count
        if total == 0:
            return 50.0  # Neutral

        # Calculate score
        score = ((positive_count - negative_count) / len(words)) * 1000 + 50
        return max(0.0, min(100.0, score))

    @staticmethod
    def _calculate_readability(text: str) -> float:
        """
        Calculate readability score based on sentence and word complexity.
        Returns score from 0 to 100.
        """
        if not text:
            return 50.0

        # Count sentences (rough approximation)
        sentences = len(re.split(r'[.!?]+', text))
        if sentences == 0:
            return 50.0

        words = text.split()
        if not words:
            return 50.0

        # Average words per sentence
        avg_words_per_sentence = len(words) / sentences

        # Penalize very long or very short sentences
        if 10 <= avg_words_per_sentence <= 20:
            readability = 100.0
        elif 5 <= avg_words_per_sentence < 10 or 20 < avg_words_per_sentence <= 30:
            readability = 80.0
        else:
            readability = 60.0

        return readability

    @staticmethod
    def _extract_key_phrases(text: str, max_phrases: int = 5) -> List[str]:
        """Extract key phrases from text."""
        if not text:
            return []

        # Simple n-gram extraction (2-3 word phrases)
        normalized = TextAnalysisService.normalize_text(text)
        words = normalized.split()

        phrases = []

        # Extract 2-grams
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            if len(phrase) > 6:  # Minimum phrase length
                phrases.append(phrase)

        # Extract 3-grams
        for i in range(len(words) - 2):
            phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
            if len(phrase) > 10:  # Minimum phrase length
                phrases.append(phrase)

        # Count and return most common
        phrase_counts = Counter(phrases)
        return [phrase for phrase, count in phrase_counts.most_common(max_phrases)]

    @staticmethod
    def calculate_skill_match_score(
        candidate_skills: SkillExtraction,
        vacancy_skills: SkillExtraction,
    ) -> Dict[str, float]:
        """
        Calculate detailed skill matching scores.
        Returns dict with scores for each skill category.
        """
        scores = {}

        # Technical skills
        if vacancy_skills.technical_skills:
            matched = len(candidate_skills.technical_skills.intersection(
                vacancy_skills.technical_skills
            ))
            required = len(vacancy_skills.technical_skills)
            scores['technical'] = (matched / required * 100) if required > 0 else 100.0
        else:
            scores['technical'] = 100.0

        # Frameworks
        if vacancy_skills.frameworks:
            matched = len(candidate_skills.frameworks.intersection(
                vacancy_skills.frameworks
            ))
            required = len(vacancy_skills.frameworks)
            scores['frameworks'] = (matched / required * 100) if required > 0 else 100.0
        else:
            scores['frameworks'] = 100.0

        # Tools
        if vacancy_skills.tools:
            matched = len(candidate_skills.tools.intersection(
                vacancy_skills.tools
            ))
            required = len(vacancy_skills.tools)
            scores['tools'] = (matched / required * 100) if required > 0 else 100.0
        else:
            scores['tools'] = 100.0

        # Methodologies
        if vacancy_skills.methodologies:
            matched = len(candidate_skills.methodologies.intersection(
                vacancy_skills.methodologies
            ))
            required = len(vacancy_skills.methodologies)
            scores['methodologies'] = (matched / required * 100) if required > 0 else 100.0
        else:
            scores['methodologies'] = 100.0

        # Soft skills
        if vacancy_skills.soft_skills:
            matched = len(candidate_skills.soft_skills.intersection(
                vacancy_skills.soft_skills
            ))
            required = len(vacancy_skills.soft_skills)
            scores['soft_skills'] = (matched / required * 100) if required > 0 else 100.0
        else:
            scores['soft_skills'] = 100.0

        return scores
