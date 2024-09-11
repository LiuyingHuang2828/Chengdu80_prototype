import React from 'react'
import styled from 'styled-components'
import { Link } from 'react-router-dom'

const CardsContainer = styled(Link)`
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 10px;
    padding: 10px;
    width: calc(100% - 20px);
    border-radius: 10px;
    border: 2px solid rgba(255, 255, 255, 1);
    background-color: rgba(255, 105, 180, 1);

    h5 {
        font-size: 20px;
        font-weight: 600;
        color: white;
        margin: 0;
    }

    p {
        font-size: 16px;
        font-weight: 400;
        color: white;
    }
`;

const Cards = ({
    name,
    desciption,
    href
}) => {
    return (
        <CardsContainer to={href}>
            <h5>
                {name}
            </h5>
            <p>
                {desciption}
            </p>
        </CardsContainer>
    )
}

export default Cards
