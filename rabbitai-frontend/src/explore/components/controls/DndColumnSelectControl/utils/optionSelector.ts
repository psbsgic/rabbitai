import { ColumnMeta } from '@superset-ui/chart-controls';
import { ensureIsArray } from '@superset-ui/core';

export class OptionSelector {
  values: ColumnMeta[];

  options: { string: ColumnMeta };

  multi: boolean;

  constructor(
    options: { string: ColumnMeta },
    multi: boolean,
    initialValues?: string[] | string,
  ) {
    this.options = options;
    this.multi = multi;
    this.values = ensureIsArray(initialValues)
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

  has(value: string): boolean {
    return !!this.getValues()?.includes(value);
  }

  getValues(): string[] | string | undefined {
    if (!this.multi) {
      return this.values.length > 0 ? this.values[0].column_name : undefined;
    }
    return this.values.map(option => option.column_name);
  }
}
