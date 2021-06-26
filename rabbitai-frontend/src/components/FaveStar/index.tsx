

import React, { useCallback } from 'react';
import { t, styled } from '@rabbitai-ui/core';
import { Tooltip } from 'src/components/Tooltip';
import { useComponentDidMount } from 'src/common/hooks/useComponentDidMount';
import Icon from '../Icon';

interface FaveStarProps {
  itemId: number;
  isStarred?: boolean;
  showTooltip?: boolean;
  saveFaveStar(id: number, isStarred: boolean): any;
  fetchFaveStar?: (id: number) => void;
}

const StyledLink = styled.a`
  font-size: ${({ theme }) => theme.typography.sizes.xl}px;
  display: flex;
  padding: 0 0 0 0.5em;
`;

const FaveStar = ({
  itemId,
  isStarred,
  showTooltip,
  saveFaveStar,
  fetchFaveStar,
}: FaveStarProps) => {
  useComponentDidMount(() => {
    if (fetchFaveStar) {
      fetchFaveStar(itemId);
    }
  });

  const onClick = useCallback(
    (e: React.MouseEvent) => {
      e.preventDefault();
      saveFaveStar(itemId, !!isStarred);
    },
    [isStarred, itemId, saveFaveStar],
  );

  const content = (
    <StyledLink
      href="#"
      onClick={onClick}
      className="fave-unfave-icon"
      data-test="fave-unfave-icon"
      role="button"
    >
      <Icon name={isStarred ? 'favorite-selected' : 'favorite-unselected'} />
    </StyledLink>
  );

  if (showTooltip) {
    return (
      <Tooltip
        id="fave-unfave-tooltip"
        title={t('Click to favorite/unfavorite')}
      >
        {content}
      </Tooltip>
    );
  }

  return content;
};
export default FaveStar;
