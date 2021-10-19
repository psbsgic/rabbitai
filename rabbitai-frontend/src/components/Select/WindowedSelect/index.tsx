import Select from 'react-select';
import Async from 'react-select/async';
import Creatable from 'react-select/creatable';
import AsyncCreatable from 'react-select/async-creatable';
import windowed from './windowed';

export * from './windowed';

export const WindowedSelect = windowed(Select);
export const WindowedAsyncSelect = windowed(Async);
export const WindowedCreatableSelect = windowed(Creatable);
export const WindowedAsyncCreatableSelect = windowed(AsyncCreatable);
export default WindowedSelect;
