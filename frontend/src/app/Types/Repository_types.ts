export interface RespositoryTypes {
  id: number;
  name: string;
  full_name?: string;
}

export interface RepositoryListProps {
  repositories: RespositoryTypes[];
  selected: RespositoryTypes;
  setSelected: (selected: RespositoryTypes) => void;
}