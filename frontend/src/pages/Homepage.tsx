import React, { useState, useEffect, useContext, useRef } from 'react';
import axios from "../Axios";
import { Link } from 'react-router-dom';
import { backendUrl } from '../shared';
import { AuthContext } from '../context/Context';
import { ImagePreviewGrid, Image  } from '../components/ImagePreviewCard';

const Homepage = () => {
    const fileInputRef = useRef<HTMLInputElement | null>(null);

    const { isLoggedIn } = useContext(AuthContext);
    
    const [files, setFiles] = useState<Image[] | []>([]);
    const [file, setFile] = useState<null | File>(null);
    const [fileName, setFileName] = useState('');
    //const [preview, setPreview] = useState<string | null>(null);

    useEffect(() => {
        if(!isLoggedIn){
            return;
        }
        // Fetch files from the backend
        axios.get(backendUrl + '/api/files/')
            .then(response => setFiles(response.data.files))
            .catch(error => console.error('Error fetching files:', error));
    }, [isLoggedIn]);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            const selectedFile = event.target.files[0];
            setFile(selectedFile);
            //setPreview(URL.createObjectURL(selectedFile));
        }
    };

    const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setFileName(event.target.value);
    };

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const formData = new FormData();
        if (file) {
            formData.append('file', file);
        }
        formData.append('name', fileName);

        // Upload file to the backend
        axios.post<Image>(backendUrl + '/api/files/', formData)
            .then(response => {
                // Refresh the files list
                setFiles([...files, response.data]);
                setFile(null);
                setFileName('');
                //setPreview(null);
                if (fileInputRef.current) {
                    fileInputRef.current.value = ''; // Clear file input
                }
            })
            .catch(error => console.error('Error uploading file:', error));
    };

    if (isLoggedIn) {
        return (
            <div>
                <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', maxWidth: '300px', margin: 'auto' }}>
                    <input type="file" ref={fileInputRef} onChange={handleFileChange} style={{ marginBottom: '10px' }} />
                    <input type="text" placeholder="Enter file name" value={fileName} onChange={handleNameChange} style={{ marginBottom: '10px' }} />
                    <button type="submit" style={{ padding: '10px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '5px' }}>Upload</button>
                </form>
                {/*preview && <ImagePreviewCard imageUrl={preview} />*/}
                <div>
                    {files ? 
                        // <div key={index}>
                        //     <a href={backendUrl + file.file} download>{file.name}</a>
                        //     <img src={backendUrl + file.file} alt={file.name} style={{ maxWidth: '100px', display: 'block', marginTop: '10px' }} />
                        // </div>
                        <ImagePreviewGrid images={files}/>
                    : ''}
                </div>
            </div>
        );
    } else {
        return <div>Please <Link to="/login">login</Link> to upload files.</div>
    }
};

export default Homepage;