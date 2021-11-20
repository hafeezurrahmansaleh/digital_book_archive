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

// const data = [
//     {
//         month: "JAN",
//         subscription: 4000,
//     },
//     {
//         month: "FEB",
//         subscription: 3000,
//         amt: 2210
//     },
//     {
//         month: "MAR",
//         subscription: 2000,
//         amt: 2290
//     },
//     {
//         month: "APR",
//         subscription: 2780,
//         amt: 2000
//     },
//     {
//         month: "MAY",
//         subscription: 1890,
//         amt: 2181
//     },
//     {
//         month: "JUN",
//         subscription: 2390,
//         amt: 2500
//     },
//     {
//         month: "JUL",
//         subscription: 3490,
//         amt: 2100
//     },
//     {
//         month: "AUG",
//         subscription: 3490,
//         amt: 2100
//     },
//     {
//         month: "SEP",
//         subscription: 3490,
//         amt: 2100
//     }
// ];



const SubscribeChart = () => {
    const [subscribePerYear, setSubscribePerYear] = useState([]);
    const [startDate, setStartDate] = useState(new Date());


    useEffect(() => {
        axios.get(`http://127.0.0.1:8000/api/v1/dashboard/SubscriptionChart/?year=${startDate.getFullYear()}`)
            .then(res => setSubscribePerYear(res.data))
            .catch(err => console.log(err))
    }, [startDate]);

    return (
        <div className="mt-5">
            <div className="text-start ms-5 mb-3" style={{ maxWidth: 300 }}>
                <div class="d-flex border">
                    <div class="px-4 fs-5 d-flex align-items-center bg-light" id="inputGroup-sizing-default">Year</div>
                    <DatePicker
                        className="form-control border-0 fs-5"
                        selected={startDate}
                        onChange={(date) => setStartDate(date)}
                        dateFormat="yyyy"
                        showYearPicker
                    />
                </div>
                
            </div>
            <ResponsiveContainer width={'100%'} height={400}>
                <AreaChart
                    // width={500}
                    // height={400}
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