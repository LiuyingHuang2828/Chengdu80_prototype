import React, { useState } from 'react'
import Background from '../components/background/Background';
import Header from '../components/containers/Header';
import Body from '../components/containers/Body';
import Input from '../components/inputs/Input';
import Button from '../components/button/Button';
import NewContainer from '../components/containers/NewContainer';
import NewsBody from '../components/containers/NewsBody';
import Cards from '../components/cards/Cards';


import { post, get } from 'aws-amplify/api';

const Home = () => {
    const [company, setCompany] = useState('');
    const [loanRisk, setLoanRisk] = useState([]);
    const [legalRisk, setLegalRisk] = useState([]);
    const [operationalRisk, setOperationalRisk] = useState([]);
    const [othersRisk, setOthersRisk] = useState([]);

    const getNewsData = async () => {
        try {
            const { body } = await get({
                apiName: 'fetchNewsApi',
                path: `/fetch-news/${company.toLowerCase()}`,
            }).response;

            const data = await body.json();

            // sort the data into different categories
            data.filter((news) => {
                if (news.riskCategory === 'loan risk') {
                    setLoanRisk(news.article);
                } else if (news.riskCategory === 'legal risk') {
                    setLegalRisk(news.article);
                } else if (news.riskCategory === 'operational risk') {
                    setOperationalRisk(news.article);
                } else {
                    setOthersRisk(news.article);
                }
            });

            console.log(legalRisk, loanRisk, operationalRisk, othersRisk);

        } catch (error) {
            console.error(error);
        }
    }


    const findNewsData = async () => {
        try {
            await post({
                apiName: 'fetchNewsApi',
                path: '/fetch-news',
                options: {
                    body: {
                        company_name: company.toLowerCase()
                    }
                }
            }).response;

            await getNewsData();
        } catch (error) {
            console.error(error);
        }
    }

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
                <Button name="Analyze" onClick={findNewsData} />
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
                    <h4>
                        Legal
                    </h4>
                    {legalRisk.length === 0 && <p>
                        Sorry, no articles found for this section
                    </p>}
                    <NewsBody>
                        {legalRisk.map((news, index) => (
                            <Cards key={index} name={news.title} desciption={news.description} href={news.url} author={news.author} publicatedAt={news.publishedAt} source={news.source.name} urlToImage={news.urlToImage} />
                        ))}
                    </NewsBody>
                    <h4>
                        Loan
                    </h4>
                    {loanRisk.length === 0 && <p>
                        Sorry, no articles found for this section
                    </p>}
                    <NewsBody>
                        {loanRisk.map((news, index) => (
                            <Cards key={index} name={news.title} desciption={news.description} href={news.url} author={news.author} publicatedAt={news.publishedAt} source={news.source.name} urlToImage={news.urlToImage} />
                        ))}
                    </NewsBody>
                    <h4>
                        Operational
                    </h4>
                    {operationalRisk.length === 0 && <p>
                        Sorry, no articles found for this section
                    </p>}
                    <NewsBody>
                        {operationalRisk.map((news, index) => (
                            <Cards key={index} name={news.title} desciption={news.description} href={news.url} author={news.author} publicatedAt={news.publishedAt} source={news.source.name} urlToImage={news.urlToImage} />
                        ))}
                    </NewsBody>
                    <h4>
                        Others
                    </h4>
                    {othersRisk.length === 0 && <p>
                        Sorry, no articles found for this section
                    </p>}
                    <NewsBody>
                        {othersRisk.map((news, index) => (
                            <Cards key={index} name={news.title} desciption={news.description} href={news.url} author={news.author} publicatedAt={news.publishedAt} source={news.source.name} urlToImage={news.urlToImage} />
                        ))}
                    </NewsBody>
                </NewContainer>
            </Body>
        </Background>
    )
}

export default Home
