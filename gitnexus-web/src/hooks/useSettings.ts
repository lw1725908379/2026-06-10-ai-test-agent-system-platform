// @ts-expect-error  MC8yOmFIVnBZMlhsaUpqbWxvYzZaRFZZZGc9PTplZGRkNThhMg==

import { useAppState } from './useAppState';
// NOTE  MS8yOmFIVnBZMlhsaUpqbWxvYzZaRFZZZGc9PTplZGRkNThhMg==

export const useSettings = () => {
  const { llmSettings, updateLLMSettings } = useAppState();

  return {
    settings: llmSettings,
    updateSettings: updateLLMSettings,
  };
};
