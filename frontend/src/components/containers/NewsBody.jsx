import React from 'react'
import styled from 'styled-components'

const NewsBodyContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 7px;
`;

const NewsBody = ({ children }) => {
    return (
        <NewsBodyContainer>
            {children}
        </NewsBodyContainer>
    )
}

export default NewsBody
