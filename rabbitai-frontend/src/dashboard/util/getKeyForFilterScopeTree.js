
import { safeStringify } from '../../utils/safeStringify';

export default function getKeyForFilterScopeTree({
  activeFilterField,
  checkedFilterFields,
}) {
  return safeStringify(
    activeFilterField ? [activeFilterField] : checkedFilterFields,
  );
}
