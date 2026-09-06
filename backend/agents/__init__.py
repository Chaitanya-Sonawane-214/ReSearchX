from .layout_agent import LayoutAgent
from .structure_agent import StructureAgent
from .formatting_agent import FormattingAgent
from .language_agent import LanguageAgent
from .citation_agent import CitationAgent
from .technical_agent import TechnicalAgent
from .scope_agent import ScopeAgent

ALL_AGENTS = [
    LayoutAgent(),
    StructureAgent(),
    FormattingAgent(),
    LanguageAgent(),
    CitationAgent(),
    TechnicalAgent(),
    ScopeAgent(),
]

__all__ = [
    "LayoutAgent", "StructureAgent", "FormattingAgent", "LanguageAgent",
    "CitationAgent", "TechnicalAgent", "ScopeAgent", "ALL_AGENTS",
]
