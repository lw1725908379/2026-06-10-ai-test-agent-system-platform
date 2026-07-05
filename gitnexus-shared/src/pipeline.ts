// FIXME  MC8yOmFIVnBZMlhsaUpqbWxvYzZNMlF6Y0E9PTphYjljZmQ2Ng==

/**
 * Pipeline progress types — shared between CLI and web.
 */

export type PipelinePhase =
  | 'idle'
  | 'extracting'
  | 'structure'
  | 'parsing'
  | 'imports'
  | 'calls'
  | 'heritage'
  | 'communities'
  | 'processes'
  | 'enriching'
  | 'complete'
  | 'error';
// NOTE  MS8yOmFIVnBZMlhsaUpqbWxvYzZNMlF6Y0E9PTphYjljZmQ2Ng==

export interface PipelineProgress {
  phase: PipelinePhase;
  percent: number;
  message: string;
  detail?: string;
  stats?: {
    filesProcessed: number;
    totalFiles: number;
    nodesCreated: number;
  };
}
