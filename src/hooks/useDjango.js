import React, { useEffect, useState } from 'react';
import jwt_decode from "jwt-decode";
import axios from 'axios';

const useDjango = () => {

    const [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null)
    const [user, setUser] = useState({})
    const [isExpire, setIsExpire] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const [authError, setAuthError] = useState('');

    let loginUser = async (phone, password, location, history) => {
        let response = await fetch('http://127.0.0.1:8000/api/v1/auth/api-token-auth/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'phone': phone, 'password': password })
        })
        let data = await response.json()

        if (response.status === 200) {
            setAuthTokens(data);
            setUpUser(data, true);
            localStorage.setItem('authTokens', JSON.stringify(data));
            const destination = location?.state?.from || '/dashboard';
            history.replace(destination);
            setAuthError('');
        } else {
            setAuthError('Phone number or password is invalid')
        }
    }


    let logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
    }


    let updateToken = async () => {

        let response = await fetch('http://127.0.0.1:8000/api/v1/auth/token-refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'refresh': authTokens?.refresh })
        })

        let data = await response.json()

        if (response.status === 200) {
            setAuthTokens(data)
            setUpUser(data, false)
            localStorage.setItem('authTokens', JSON.stringify(data))
        } else {
            logoutUser()
        }

    }

    const setUpUser = (data, isFirst) => {
        const token = jwt_decode(data.access)
        const userId = token['user_id']
        isFirst && setIsLoading(true)
        const userData = { user_id: userId }
        axios.post('http://127.0.0.1:8000/api/v1/dashboard/get_user/', userData, {
            headers: {
                Authorization: 'Bearer ' + String(data?.access)
            }
        })
            .then(res => setUser(res.data))
            .catch(err => console.log(err))
            .finally(() => {
                setIsLoading(false)
                setIsExpire(false)
            })
    }


    useEffect(() => {

        if (isLoading && authTokens) {
            updateToken()
        }
        else if (isLoading && !authTokens) {
            setIsLoading(false)
        }
        let fourMinutes = 1000 * 60 * 4

        let interval = setInterval(() => {
            if (authTokens) {
                updateToken()
            }
        }, fourMinutes)
        return () => clearInterval(interval)

    }, [authTokens, isExpire])

    return {
        user,
        authTokens,
        loginUser,
        logoutUser,
        isLoading,
        authError
    }
}

export default useDjango;