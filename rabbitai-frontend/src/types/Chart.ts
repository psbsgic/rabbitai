/**
 * The Chart model as returned from the API
 */

import { QueryFormData } from '@rabbitai-ui/core';
import Owner from './Owner';

export interface Chart {
  id: number;
  url: string;
  viz_type: string;
  slice_name: string;
  creator: string;
  changed_on: string;
  changed_on_delta_humanized?: string;
  changed_on_utc?: string;
  description: string | null;
  cache_timeout: number | null;
  thumbnail_url?: string;
  owners?: Owner[];
  datasource_name_text?: string;
}

export type Slice = {
  id?: number;
  slice_id: number;
  slice_name: string;
  description: string | null;
  cache_timeout: number | null;
  form_data?: QueryFormData;
};

export default Chart;
