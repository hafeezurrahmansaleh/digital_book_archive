import axios from 'axios';
import React, { useEffect, useState } from 'react';
import {
    AreaChart,
    Area,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer
} from "recharts";
import DatePicker from "react-datepicker";
import useAuth from '../../../hooks/useAuth';



const SubscribeChart = () => {
    const [subscribePerYear, setSubscribePerYear] = useState([]);
    const [startDate, setStartDate] = useState(new Date());
    const { authTokens } = useAuth();

    useEffect(() => {
        axios.get(`http://127.0.0.1:8000/api/v1/dashboard/SubscriptionChart/?year=${startDate.getFullYear()}`, {
            headers: {
                Authorization: 'Bearer ' + String(authTokens?.access)
            }
        })
            .then(res => setSubscribePerYear(res.data))
            .catch(err => console.log(err))
    }, [startDate]);

    return (
        <div className="mt-5">
            <div className="text-start ms-5 mb-3" style={{ maxWidth: 300 }}>
                <div class="d-flex border rounded-pill border-2">
                    <div class="px-4 fs-5 d-flex align-items-center bg-light rounded-pill" id="inputGroup-sizing-default">Year</div>
                    <DatePicker
                        className="form-control border-0 fs-5 rounded-pill"
                        selected={startDate}
                        onChange={(date) => setStartDate(date)}
                        dateFormat="yyyy"
                        showYearPicker
                    />
                </div>
                
            </div>
            <ResponsiveContainer width={'100%'} height={400}>
                <AreaChart
                    data={subscribePerYear}
                    margin={{
                        top: 10,
                        right: 30,
                        left: 0,
                        bottom: 0
                    }}
                >
                    <CartesianGrid vertical={false} stroke="#DDD" />
                    <defs>
                        <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#FFFFFF" stopOpacity={0.5} />
                        </linearGradient>
                    </defs>
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="subscription" stroke="#8884d8" fill="url(#colorUv)" dot={true} />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
};

export default SubscribeChart;