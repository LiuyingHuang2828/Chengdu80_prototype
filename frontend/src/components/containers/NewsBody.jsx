import React from 'react'
import styled from 'styled-components'

const NewsBodyContainer = styled.div`
    display: flex;
    flex-direction: row;
    width: 100%;
    overflow-x: auto;
    gap: 10px;
    padding: 10px 5px;
`;

const NewsBody = ({ children }) => {
    return (
        <NewsBodyContainer>
            {children}
        </NewsBodyContainer>
    )
}

export default NewsBody
