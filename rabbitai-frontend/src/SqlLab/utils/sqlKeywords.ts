
import { SQL_KEYWORD_AUTOCOMPLETE_SCORE } from '../constants';

const SQL_KEYWORDS = [
  'AND',
  'AS',
  'ASC',
  'AVG',
  'BY',
  'CASE',
  'COUNT',
  'CREATE',
  'CROSS',
  'DATABASE',
  'DEFAULT',
  'DELETE',
  'DESC',
  'DISTINCT',
  'DROP',
  'ELSE',
  'END',
  'FOREIGN',
  'FROM',
  'GRANT',
  'GROUP',
  'HAVING',
  'IF',
  'INNER',
  'INSERT',
  'JOIN',
  'KEY',
  'LEFT',
  'LIMIT',
  'MAX',
  'MIN',
  'NATURAL',
  'NOT',
  'NULL',
  'OFFSET',
  'ON',
  'OR',
  'ORDER',
  'OUTER',
  'PRIMARY',
  'REFERENCES',
  'RIGHT',
  'SELECT',
  'SUM',
  'TABLE',
  'THEN',
  'TYPE',
  'UNION',
  'UPDATE',
  'WHEN',
  'WHERE',
];

const SQL_DATA_TYPES = [
  'BIGINT',
  'BINARY',
  'BIT',
  'CHAR',
  'DATE',
  'DECIMAL',
  'DOUBLE',
  'FLOAT',
  'INT',
  'INTEGER',
  'MONEY',
  'NUMBER',
  'NUMERIC',
  'REAL',
  'SET',
  'TEXT',
  'TIMESTAMP',
  'VARCHAR',
];

const allKeywords = SQL_KEYWORDS.concat(SQL_DATA_TYPES);

const sqlKeywords = allKeywords.map(keyword => ({
  meta: 'sql',
  name: keyword,
  score: SQL_KEYWORD_AUTOCOMPLETE_SCORE,
  value: keyword,
}));

export default sqlKeywords;
