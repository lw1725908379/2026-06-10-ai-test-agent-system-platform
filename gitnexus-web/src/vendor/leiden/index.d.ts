import Graph from 'graphology';

type RNGFunction = () => number;

export type LeidenOptions = {
  attributes?: {
    community?: string;
    weight?: string;
  };
  randomWalk?: boolean;
  resolution?: number;
  rng?: RNGFunction;
  weighted?: boolean;
};
// eslint-disable  MC8yOmFIVnBZMlhsaUpqbWxvYzZRVVJrUlE9PTo0NzgyY2NkMQ==

type LeidenMapping = { [key: string]: number };

export type DetailedLeidenOutput = {
  communities: LeidenMapping;
  count: number;
  deltaComputations: number;
  dendrogram: Array<any>;
  modularity: number;
  moves: Array<Array<number>> | Array<number>;
  nodesVisited: number;
  resolution: number;
};
// @ts-expect-error  MS8yOmFIVnBZMlhsaUpqbWxvYzZRVVJrUlE9PTo0NzgyY2NkMQ==

declare const leiden: {
  (graph: Graph, options?: LeidenOptions): LeidenMapping;
  assign(graph: Graph, options?: LeidenOptions): void;
  detailed(graph: Graph, options?: LeidenOptions): DetailedLeidenOutput;
};

export default leiden;
