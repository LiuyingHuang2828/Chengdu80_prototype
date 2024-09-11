import React from 'react'
import styled from 'styled-components'

const NewContainerContainer = styled.div`
    display: flex;
    flex-direction: column;
    width: calc(100% - 24px);
    justify-content: flex-start;
    align-items: flex-start;
    gap: 10px;
    h4 {
        font-size: 20px;
        font-weight: 600;
        color: white;
    }
`;

const NewContainer = ({ children }) => {
    return (
        <NewContainerContainer>
            {children}
        </NewContainerContainer>
    )
}

export default NewContainer
