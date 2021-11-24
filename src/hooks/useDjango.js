import React, { useEffect, useState } from 'react';
import jwt_decode from "jwt-decode";

const useDjango = () => {

    const [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null)
    const [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwt_decode(localStorage.getItem('authTokens')) : null)
    // const [user, setUser] = useState({})
    const [isLoading, setIsLoading] = useState(true)
    const [authError, setAuthError] = useState('');


    let loginUser = async (phone, password, location, history) => {
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
            const destination = location?.state?.from || '/dashboard';
            history.replace(destination);
            setAuthError('');
            // history.push('/dashboard');
        } else {
            setAuthError('Something went wrong!')
            // alert('Something went wrong!');
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

        if (isLoading) {
            setIsLoading(false)
        }
    }


    useEffect(() => {

        if (isLoading) {
            updateToken()
        }

        let fourMinutes = 1000 * 60 * 4

        let interval = setInterval(() => {
            if (authTokens) {
                // setUser() to be continue....
                updateToken()
            }
        }, fourMinutes)
        return () => clearInterval(interval)

    }, [authTokens, isLoading])

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