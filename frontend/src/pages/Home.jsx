import React, { useState } from 'react'
import Background from '../components/background/Background';
import Header from '../components/containers/Header';
import Body from '../components/containers/Body';
import Input from '../components/inputs/Input';
import Button from '../components/button/Button';
import NewContainer from '../components/containers/NewContainer';
import NewsBody from '../components/containers/NewsBody';
import Cards from '../components/cards/Cards';


const Home = () => {
    const [company, setCompany] = useState('');

    return (
        <Background>
            <Header>
                <h1>
                    Corporate Analysis
                </h1>
                <h2>
                    Risk Analysis using News and LLMs
                </h2>
                <p>
                    Using freshly fetch news and categorize it into different categories to analyze the risk of a company.
                    We will then use LLMs to summarize each category and provide a risk analysis, give a score to each category and provide a final risk score.
                </p>
            </Header>
            <Body>
                <h3>
                    Enter a company name
                </h3>
                <Input placeholder="Company Name" type="text" onChange={(e) => setCompany(e.target.value)} value={company} />
                <Button name="Analyze" onClick={() => console.log(company)} />
            </Body>
            <Body>
                <>
                    <h3>
                        News Fetched
                    </h3>
                    <p>
                        News fetched will be categorized into 4 types of categories of risk: legal, loan, operational and others.
                    </p>
                </>
                <NewContainer>
                    <NewsBody>
                        <h4>
                            Legal
                        </h4>
                    </NewsBody>
                    <NewsBody>
                        <h4>
                            Loan
                        </h4>
                    </NewsBody>
                    <NewsBody>
                        <h4>
                            Operational
                        </h4>
                    </NewsBody>
                    <NewsBody>
                        <h4>
                            Others
                        </h4>
                    </NewsBody>
                </NewContainer>
            </Body>
        </Background>
    )
}

export default Home
