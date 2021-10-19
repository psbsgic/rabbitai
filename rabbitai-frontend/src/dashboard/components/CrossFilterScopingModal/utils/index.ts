import { FormInstance } from 'antd/lib/form';

// eslint-disable-next-line import/prefer-default-export
export const setCrossFilterFieldValues = (
  form: FormInstance,
  values: object,
) => {
  form.setFieldsValue({
    ...values,
  });
};
