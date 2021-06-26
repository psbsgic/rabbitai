
import React from 'react';
import { useStaticQuery, graphql } from 'gatsby';
import Img from 'gatsby-image';

interface Props {
  imageName?: string;
  width?: string;
  height?: string;
  otherProps?: any;
}

const Image = ({
  imageName, width, height, ...otherProps
}: Props) => {
  const data = useStaticQuery(graphql`
    query {
      logoSm: file(relativePath: { eq: "src/images/s.png" }) {
        childImageSharp {
          fixed(height: 30) {
            ...GatsbyImageSharpFixed
          }
        }
      }

      logoLg: file(relativePath: { eq: "src/images/s.png" }) {
        childImageSharp {
          fixed(width: 150) {
            ...GatsbyImageSharpFixed
          }
        }
      }

      stackoverflow: file(
        relativePath: { eq: "src/images/stack_overflow.png" }
      ) {
        childImageSharp {
          fixed(width: 60) {
            ...GatsbyImageSharpFixed
          }
        }
      }

      docker: file(relativePath: { eq: "src/images/docker.png" }) {
        childImageSharp {
          fixed(width: 100) {
            ...GatsbyImageSharpFixed
          }
        }
      }

      preset: file(relativePath: { eq: "src/images/preset.png" }) {
        childImageSharp {
          fixed(width: 100) {
            ...GatsbyImageSharpFixed
          }
        }
      }
    }
  `);

  return <Img fixed={data[imageName]?.childImageSharp?.fixed} {...otherProps} />;
};

export default Image;
