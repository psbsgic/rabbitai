
type CreatedByUser = {
  id: number;
  first_name: string;
  last_name: string;
};

export type TemplateObject = {
  id?: number;
  changed_on_delta_humanized?: string;
  created_on?: string;
  created_by?: CreatedByUser;
  css?: string;
  template_name: string;
};
