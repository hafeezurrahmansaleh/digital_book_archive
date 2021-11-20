import React, { useEffect, useState } from 'react';
import jwt_decode from "jwt-decode";
import { useHistory } from 'react-router';

const useDjango = () => {

    const [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null)
    const [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwt_decode(localStorage.getItem('authTokens')) : null)
    const [loading, setLoading] = useState(true)

    const history = useHistory()

    let loginUser = async (phone, password) => {
        // e.preventDefault()
        let response = await fetch('http://127.0.0.1:8000/api/v1/auth/api-token-auth/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'phone': phone, 'password': password })
        })
        let data = await response.json()
        console.log(data)

        if (response.status === 200) {
            setAuthTokens(data);
            setUser(jwt_decode(data.access));
            localStorage.setItem('authTokens', JSON.stringify(data));
            // history.push('/dashboard');
        } else {
            alert('Something went wrong!');
        }
    }


    let logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
        // history.push('/login');
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
            setUser(jwt_decode(data.access))
            localStorage.setItem('authTokens', JSON.stringify(data))
        } else {
            logoutUser()
        }

        if (loading) {
            setLoading(false)
        }
    }

    // let contextData = {
    //     user: user,
    //     authTokens: authTokens,
    //     loginUser: loginUser,
    //     logoutUser: logoutUser,
    // }


    useEffect(() => {

        if (loading) {
            updateToken()
        }

        let fourMinutes = 1000 * 60 * 4

        let interval = setInterval(() => {
            if (authTokens) {
                updateToken()
            }
        }, fourMinutes)
        return () => clearInterval(interval)

    }, [authTokens, loading])

    return {
        user,
        authTokens,
        loginUser,
        logoutUser
    }
}

export default useDjango;