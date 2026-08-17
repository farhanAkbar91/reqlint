export interface SmellResult {
  rule_id: string;
  category: 'Ambiguity' | 'Incompleteness' | 'Unverifiable';
  severity: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  message: string;
  target_text: string;
  start_char: number;
  end_char: number;
}

export interface RevisionSuggestion {
  original_text: string;
  suggested_text: string;
  rationale: string;
  framework: string;
}

export interface AuditResponse {
  requirement_text: string;
  detected_language: 'id' | 'en' | 'unknown';
  quality_score: number;
  ambiguity_index: number;
  completeness_score: number;
  verifiability_score: number;
  smells: SmellResult[];
  revisions: RevisionSuggestion[];
}
