import React from 'react';
import styled from 'styled-components';

const FormContainer = styled.div`
    display: flex;
    flex-direction: row;
    flex: 1;
    width: 100%;
    position: relative;

    .input-wrapper {
        position: relative;
        width: 100%;
        margin: 0px auto 10px;
    }

    .underline {
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 2px;
        background-color: rgba(255, 105, 180, 1);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.5s ease-in-out;
    }

    .input-box {
        font-size: 20px;
        font-weight: 500;
        padding: 10px 0;
        border: none;
        border-bottom: 2px solid #ccc;
        color: white;
        width: 100%;
        font-family: 'Montserrat', sans-serif;
        background-color: transparent;
        transition: border-color 0.5s ease-in-out;
    }

    .input-box:focus {
        outline: none;
    }
      
    .input-box:focus + .underline {
        transform: scaleX(1);
    }
`;

const Input = ({ placeholder, value, onChange, type }) => {
    return (
        <FormContainer>
            <div className="input-wrapper">
                <input className="input-box" type={type} placeholder={placeholder} value={value} onChange={onChange} />
                <span className="underline"></span>
            </div>
        </FormContainer>
    );
};

export default Input;