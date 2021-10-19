import React from 'react';
import { useStaticQuery, graphql } from 'gatsby';
import Img from 'gatsby-image';

interface Props {
  imageName?: string;
}

const DbImage = ({ imageName }: Props) => {
  const data = useStaticQuery(graphql`
    query {
      allImages: allFile(filter: {relativeDirectory: {eq: "src/images/databases"}}) {
        edges {
          node {
            childImageSharp {
              fixed(height: 50) {
                ...GatsbyImageSharpFixed
                originalName
              }
            }
          }
        }
      }
    }
  `);
  const images = data.allImages.edges.map((img) => img.node?.childImageSharp?.fixed);
  const filter = images.filter((img) => img?.originalName === imageName);
  return <Img fixed={filter[0]} />;
};

export default DbImage;
