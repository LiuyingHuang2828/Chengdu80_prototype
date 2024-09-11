import React from 'react'
import styled from 'styled-components'

const BodyContainer = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    width: 100%;
    gap: 20px;
    margin: 5vh 0 0 0;

    h3 {
        color: white;
        text-shadow: 
            0 2px 4px rgba(255, 105, 180, 0.7),  /* Pink underglow directly below */
            0 4px 8px rgba(255, 105, 180, 0.5),  /* Soft pink glow further below */
            0 6px 12px rgba(255, 105, 180, 0.3); /* Additional soft pink glow */
    }
`;

const Body = ({ children }) => {
    return (
        <BodyContainer>
            {children}
        </BodyContainer>
    )
}

export default Body
