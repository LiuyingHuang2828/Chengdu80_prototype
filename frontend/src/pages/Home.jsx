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
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import Divider from '../components/divider/Divider';

import { post, get } from 'aws-amplify/api';

const Home = () => {
    const [company, setCompany] = useState('');
    const [loanRisk, setLoanRisk] = useState([]);
    const [legalRisk, setLegalRisk] = useState([]);
    const [operationalRisk, setOperationalRisk] = useState([]);
    const [othersRisk, setOthersRisk] = useState([]);
    const [selectedRisk, setSelectedRisk] = useState('legal risk');
    const [selectedType, setSelectedType] = useState('news');
    const [dataPoints, setDataPoints] = useState([]);
    const [riskSummary, setRiskSummary] = useState([]);
    const [mainSummary, setMainSummary] = useState('');
    const [error, setError] = useState('');

    const [step, setStep] = useState([]);

    const options = ['legal risk', 'loan risk', 'operation risk', 'other risks'];

    const selections = ['news', 'stock']

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
                } else if (news.riskCategory === 'operation risk') {
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

    const getStockData = async () => {
        try {
            const { body } = await get({
                apiName: 'stockStreamingApi',
                path: `/stock-data/${company.toLowerCase()}`,
            }).response;

            const data = await body.json();

            console.log(data);

            const stockData = data?.stock_prices

            const today = new Date();
            setDataPoints(stockData.map((value, index) => {
                const date = new Date();
                date.setMonth(today.getMonth() - (stockData.length - 1 - index)); // Adjust months instead of days
                return [
                    Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()),
                    value,
                ];
            }));

            console.log(dataPoints);

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

    const generateMainSummary = async () => {
        try {
            const { body } = await post({
                apiName: 'mainSummaryApi',
                path: '/main-summary',
                options: {
                    body: {
                        company_name: company.toLowerCase()
                    }
                }
            }).response;

            const data = await body.json();

            console.log(data);
        } catch (error) {
            console.error(error);
        }
    }

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

    const getMainSummary = async () => {
        try {
            const { body } = await get({
                apiName: 'mainSummaryApi',
                path: `/main-summary/${company.toLowerCase()}`,
            }).response;

            const data = await body.json();

            console.log(data);

            setMainSummary(data);

        } catch (error) {
            console.error(error);
        }
    }

    const findNewsData = async () => {
        try {

            setStep([]);

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

            await getStockData();

            if (loanRisk.length === 0 && legalRisk.length === 0 && operationalRisk.length === 0 && othersRisk.length === 0) {
                setError(`No News Found for ${company}, maybe there is a spelling mistake, or the company is not in the database`);
                return;
            }

            setStep([0]);

            for (let i = 0; i < options.length; i++) {
                await summarizeNews(options[i]);
            }

            await getSummary();

            setStep([0, 1]);

            await generateMainSummary();

            await getMainSummary();

            setStep([0, 1, 2]);

        } catch (error) {
            console.error(error);
        }
    }


    const linChartOptions = {
        chart: {
            backgroundColor: '#2b2b2b', // Dark background color
            width: null,
        },
        title: {
            text: `Stock Prices for ${company}`,
            style: {
                color: '#FFFFFF', // White text for the title
            },
        },
        xAxis: {
            type: 'datetime',
            dateTimeLabelFormats: {
                day: '%b %e',
            },
            labels: {
                style: {
                    color: '#FFFFFF', // White labels on the x-axis
                },
            },
            lineColor: '#FFFFFF', // White line for x-axis
            tickColor: '#FFFFFF', // White ticks on x-axis
        },
        yAxis: {
            title: {
                text: 'Value',
                style: {
                    color: '#FFFFFF', // White text for y-axis title
                },
            },
            labels: {
                style: {
                    color: '#FFFFFF', // White labels on the y-axis
                },
            },
            gridLineColor: '#505050', // Darker grid lines
        },
        legend: {
            itemStyle: {
                color: '#FFFFFF', // White text in the legend
            },
            itemHoverStyle: {
                color: '#FFFFFF', // White text on hover in the legend
            },
        },
        tooltip: {
            backgroundColor: '#2b2b2b', // Match tooltip background with chart background
            style: {
                color: '#FFFFFF', // White text in tooltips
            },
        },
        plotOptions: {
            series: {
                dataLabels: {
                    color: '#FFFFFF', // White data labels
                },
                marker: {
                    lineColor: '#333', // Marker outline color
                },
            },
        },
        series: [
            {
                name: 'Data',
                data: dataPoints,
                color: 'rgba(255, 105, 180, 1)'
            },
        ],
    };



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
                {error && <p className='error-message'>{error}</p>}
                <Button name="Analyze" onClick={findNewsData} />
            </Body>
            {step.includes(0) &&
                <Body>
                    <>
                        <h3>
                            Data Fetched
                        </h3>
                        <Selector options={selections} selected={selectedType} setOption={setSelectedType} />
                        {selectedType === 'news' &&
                            <p>
                                News fetched will be categorized into 4 types of categories of risk: legal, loan, operational and others.
                            </p>
                        }
                    </>
                    {selectedType === 'news' &&
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
                    }
                    {selectedType === 'stock' &&
                        <NewContainer>
                            <HighchartsReact highcharts={Highcharts} options={linChartOptions} />
                        </NewContainer>
                    }
                </Body>}
            {step.includes(1) &&
                <Body>
                    <Divider />
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
            {step.includes(2) &&
                <Body>
                    <Divider />
                    <h3>
                        Main Summary
                    </h3>
                    <p>
                        Using the summaries of the 4 different categories, we will provide you with a main summary and a final risk score.
                    </p>
                    {mainSummary && (<>
                        <ReactMarkdown>
                            {mainSummary}
                        </ReactMarkdown>
                    </>)}
                </Body>
            }
        </Background>
    )
}

export default Home
