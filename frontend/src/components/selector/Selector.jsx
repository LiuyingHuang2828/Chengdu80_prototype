import React from 'react'
import styled from 'styled-components'

const SelectorContainer = styled.div`
    display: flex;
    flex-direction: row;
    gap: 10px;
`;

const SelectorOption = styled.div`
    padding: 10px;
    cursor: pointer;
    border-radius: 5px;
    border: 2px solid ${({ selected }) => selected ? 'rgba(255, 105, 180, 1)' : '#fff'};
    background-color: ${({ selected }) => selected ? '#fff' : 'rgba(255, 105, 180, 1)'};
    color: ${({ selected }) => selected ? 'rgba(255, 105, 180, 1)' : '#fff'};
    font-weight: 600;
    font-size: 1.2rem;
    box-shadow: 0 0 10px rgba(255, 105, 180, 1);
    transition: all 0.3s ease;

    &:hover {
        background-color: #fff;
        color: rgba(255, 105, 180, 1);
    }

    &:active {
        transform: scale(0.9);
    }
`;


const Selector = ({
    options,
    setOption,
    selected
}) => {
    return (
        <SelectorContainer>
            {options.map((option, index) => (
                <SelectorOption
                    key={index}
                    selected={selected === option}
                    onClick={() => setOption(option)}
                >
                    {option}
                </SelectorOption>
            ))}
        </SelectorContainer>
    )
}

export default Selector
