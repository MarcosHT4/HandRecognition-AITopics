import React from 'react';
import {Button} from "@mui/material";
import {useState} from "react";
import api from "../api/images";
import example from "../images/example.jpeg";

const Form = () => {
    const [file, setFile] = useState(null);
    const [receivedImage, setReceivedImage] = useState(null);
    const [error, setError] = useState(null);
    const handleFileInputChange = (e) => {
        e.preventDefault()
        console.log(e.target.files[0])
        setFile(e.target.files[0])

    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        const formData = new FormData()
        formData.append('file', file)
        try{
            const response = await api.post('/annotate_image', formData, {
                responseType: 'blob',
            })
            console.log(response.data)
            setError(null)
            setReceivedImage(URL.createObjectURL(response.data))

        }catch (e) {
            if(e.response.status === 415) {
                setError('Please, upload a valid image file')
            }

        }
    }

    return (
        <section >
            <form onSubmit={handleSubmit} className="form">
                {receivedImage ? (
                    <img src={receivedImage} alt="receivedImage" height="500px" width="500px"/>
                ): (<img src={example} width="1000px" height="500px" alt="hands" className="hands"/>)}
                {error && <p className="error">{error}</p>}
                <div style={{marginBottom: "20px"}} className="form__div">


                    <Button
                        variant="contained"
                        component="label"
                    >
                        Upload File
                        <input
                            type="file"
                            hidden
                            onChange={handleFileInputChange}
                        />
                    </Button>

                    <Button variant="contained" type="submit">
                        Submit
                    </Button>

                </div>


            </form>

        </section>
    );
};

export default Form;