import React, { useState, useMemo } from 'react'
import ReactMarkdown from 'react-markdown';
import Background from '../components/background/Background';
import Header from '../components/containers/Header';
import Body from '../components/containers/Body';
import Input from '../components/inputs/Input';
import Button from '../components/button/Button';
import NewContainer from '../components/containers/NewContainer';
import NewsBody from '../components/containers/NewsBody';
import Cards from '../components/cards/Cards';
import Selector from '../components/selector/Selector';


import { post, get } from 'aws-amplify/api';

const Home = () => {
    const [company, setCompany] = useState('');
    const [loanRisk, setLoanRisk] = useState([]);
    const [legalRisk, setLegalRisk] = useState([]);
    const [operationalRisk, setOperationalRisk] = useState([]);
    const [othersRisk, setOthersRisk] = useState([]);
    const [selectedRisk, setSelectedRisk] = useState('legal risk');
    const [riskSummary, setRiskSummary] = useState([]);

    const [step, setStep] = useState([]);

    const options = ['legal risk', 'loan risk', 'operational risk', 'other risks'];

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

                return null;
            });

            console.log(legalRisk, loanRisk, operationalRisk, othersRisk);

        } catch (error) {
            console.error(error);
        }
    }

    const summarizeNews = async (riskCategory) => {
        try {
            const { body } = await post({
                apiName: 'riskSummaryApi',
                path: '/risk-summary',
                options: {
                    body: {
                        company_name: company.toLowerCase(),
                        risk_category: riskCategory
                    }
                }
            }).response;

            const data = await body.json();

            console.log(data);
        } catch (error) {
            console.error(error);
        }
    };

    const getSummary = async () => {
        try {
            const { body } = await get({
                apiName: 'riskSummaryApi',
                path: `/risk-summary/${company.toLowerCase()}`,
            }).response;

            const data = await body.json();

            console.log(data);

            setRiskSummary(data);

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

            setStep([0]);

            for (let i = 0; i < options.length; i++) {
                await summarizeNews(options[i]);
            }

            await getSummary();

            setStep([0, 1]);
        } catch (error) {
            console.error(error);
        }
    }

    const filteredRisks = useMemo(() => {
        console.log(riskSummary);
        return selectedRisk
            ? riskSummary.filter((risk) => risk.riskCategory === selectedRisk)
            : [];
    }, [riskSummary, selectedRisk]);

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
            {step.includes(0) &&
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
                </Body>}
            {step.includes(1) &&
                <Body>
                    <h3>
                        Risk Analysis
                    </h3>
                    <p>
                        Using the news fetched, we will provide you with 4 different summaries of the news fetched and provide you with a risk score.
                    </p>
                    <Selector options={options} selected={selectedRisk} setOption={setSelectedRisk} />
                    {riskSummary.length > 0 && (<>
                        <ReactMarkdown>
                            {filteredRisks[0]?.summary}
                        </ReactMarkdown>
                    </>)}
                    {riskSummary.length === 0 && <p>No data found</p>}
                </Body>
            }
        </Background>
    )
}

export default Home
