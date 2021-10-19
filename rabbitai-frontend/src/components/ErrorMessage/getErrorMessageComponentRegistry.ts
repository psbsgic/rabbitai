import { Registry, makeSingleton, OverwritePolicy } from '@superset-ui/core';
import { ErrorMessageComponent } from './types';

class ErrorMessageComponentRegistry extends Registry<
  ErrorMessageComponent,
  ErrorMessageComponent
> {
  constructor() {
    super({
      name: 'ErrorMessageComponent',
      overwritePolicy: OverwritePolicy.ALLOW,
    });
  }
}

const getErrorMessageComponentRegistry = makeSingleton(
  ErrorMessageComponentRegistry,
);

export default getErrorMessageComponentRegistry;
