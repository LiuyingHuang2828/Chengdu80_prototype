import React from 'react'
import styled from 'styled-components'

const BackgroundContainer = styled.div`
    background-color: #1a1a1a;
    display: flex;
    flex-direction: column;
    width: 90vw;
    height: 100%;
    justify-content: flex-start;
    align-items: center;
    padding: 10vh 5vw;
    gap: 20px;
    
`;

const Background = ({ children }) => {
    return (
        <BackgroundContainer>
            {children}
        </BackgroundContainer>
    )
}

export default Background
