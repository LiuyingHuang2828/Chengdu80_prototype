import React from 'react'
import styled from 'styled-components'

const ButtonContainer = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 10px 20px;
    background-color: rgba(255, 105, 180, 1);
    border-radius: 10px;
    border: 2px solid rgba(255, 255, 255, 1);
    box-shadow: 0 2px 10px rgba(255, 255, 255, 0.5);
    font-size: 20px;
    font-weight: 600;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
    margin: 0 0 0 auto;

    &:hover {
        box-shadow: 0 2px 10px rgba(255, 105, 180, 0.7);
        border: 2px solid rgba(255, 105, 180, 0.7);
    }

    &:active {
        transform: scale(0.95);
    }
`

const Button = ({
    name,
    onClick
}) => {
    return (
        <ButtonContainer onClick={onClick}>
            {name}
        </ButtonContainer>
    )
}

export default Button
