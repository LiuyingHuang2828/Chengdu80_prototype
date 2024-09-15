import React from 'react'
import styled from 'styled-components'
import { Link } from 'react-router-dom'

const CardsContainer = styled(Link)`
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: 10px;
    width: calc(100% - 20px);
    border-radius: 12px;
    min-width: 200px;
    background-image: url(${props => props.urlToImage});
    text-decoration: none;
    overflow: hidden;
    box-shadow: 0 0 5px rgba(255, 255, 255, 0.5);
    transition: transform 0.5s;
    max-height: 400px;
    min-height: 400px;
    min-width: 300px;

    h5 {
        font-size: 20px;
        font-weight: 600;
        color: white;
        margin: 0;

        // truncate text to only show 3 lines
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
    }

    p {
        font-size: 16px;
        font-weight: 400;
        color: white;
        text-overflow: ellipsis;   
    }

    &:hover {
        transform: scale(1.01);
        transition: transform 0.5s;
    }
`;

const Overlay = styled.div`
    background-color: rgba(0, 0, 0, 0.6);
    border-radius: 10px;
    padding: 10px;
    width: calc(100% - 20px);
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 10px;
    transition: background-color 0.5s;

    &:hover {
        background-color: rgba(0, 0, 0, 0.8);
    }
`;

const Description = styled.p`
    font-size: 16px;
    font-weight: 400;
    color: white;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 6;
    -webkit-box-orient: vertical;
`;

const Cards = ({
    name,
    desciption,
    author,
    publicatedAt,
    urlToImage,
    source,
    href
}) => {
    return (
        <CardsContainer to={href} urlToImage={urlToImage} target="_blank">
            <Overlay>
                <h5>
                    {name}
                </h5>
                <p>
                    {author}
                </p>
                <p>
                    {publicatedAt}
                </p>
                <p>
                    {source}
                </p>
                <Description>
                    {desciption}
                </Description>
            </Overlay>
        </CardsContainer>
    )
}

export default Cards
