
import { ColumnMeta } from '@rabbitai-ui/chart-controls';

export class OptionSelector {
  values: ColumnMeta[];

  options: { string: ColumnMeta };

  isArray: boolean;

  constructor(
    options: { string: ColumnMeta },
    initialValues?: string[] | string,
  ) {
    this.options = options;
    let values: string[];
    if (Array.isArray(initialValues)) {
      values = initialValues;
      this.isArray = true;
    } else {
      values = initialValues ? [initialValues] : [];
      this.isArray = false;
    }
    this.values = values
      .map(value => {
        if (value in options) {
          return options[value];
        }
        return null;
      })
      .filter(Boolean);
  }

  add(value: string) {
    if (value in this.options) {
      this.values.push(this.options[value]);
    }
  }

  del(idx: number) {
    this.values.splice(idx, 1);
  }

  replace(idx: number, value: string) {
    if (this.values[idx]) {
      this.values[idx] = this.options[value];
    }
  }

  swap(a: number, b: number) {
    [this.values[a], this.values[b]] = [this.values[b], this.values[a]];
  }

  has(groupBy: string): boolean {
    return !!this.getValues()?.includes(groupBy);
  }

  getValues(): string[] | string | undefined {
    if (!this.isArray) {
      return this.values.length > 0 ? this.values[0].column_name : undefined;
    }
    return this.values.map(option => option.column_name);
  }
}
