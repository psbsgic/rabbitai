
import React from 'react';
import { Anchor } from 'antd';
import { useMenus } from 'docz';
import { css } from '@emotion/core';
import { getActiveMenuItem, mq } from '../utils';

const { Link } = Anchor;
const anchorNavStyle = css`

    ${[mq[3]]} {
      display: none;
    }
    position: fixed;
    top: 64px;
    right: 0;
    width: 250px;
    padding: 16px;
    height: 605px;
    overflow: auto;
    ul {
      font-size: 12px;
      li {
        height: 25px;
        line-height: 25px;
        word-wrap: break-word;
      }
    }
`;

const HeaderNav = () => {
  const menus = useMenus();
  const { headings } = getActiveMenuItem(menus);
  return (
    <div css={anchorNavStyle}>
      <Anchor>
        {headings.map((e) => (
          <Link key={e.slug} href={`#${e.slug}`} title={e.value} />
        ))}
      </Anchor>
    </div>
  );
};

export default HeaderNav;
