import React, { useRef, useState } from "react";
// import "@tensorflow/tfjs-backend-cpu";
// import "@tensorflow/tfjs-backend-webgl";
// import * as cocoSsd from "@tensorflow-models/coco-ssd";

import axios from 'axios';

const ImageDetector = () => {
	const searchImage = useRef();
	const [imageData, setImageData] = useState(null)

	const openSearchImage = () => {
		if (searchImage.current) searchImage.current.click();
	}

  const readImage = (file) => {
    return new Promise((rs, rj) => {
      const fileReader = new FileReader();
      fileReader.onload = () => rs(fileReader.result);
      fileReader.onerror = () => rj(fileReader.error);
      fileReader.readAsDataURL(file);
    });
  };

	const onSelectImage = async (e) => {
		const image = e.target.files[0];
		const imageData = await readImage(image);
		setImageData(imageData);

		const imageElement = document.createElement("img");
		imageElement.src = imageData;

		imageElement.onload = async() => {
			getMatchResult(imageElement)
			await detectImageObj(imageElement);
		}
	}

	async function getMatchResult(image) {
    await axios.get(`/api/findmatch/`, image)
		.then(response => {
			console.log("match list: ", response.data)
		})
		.catch(error => {
			console.log(error)
		})
  }

	const detectImageObj = async (image) => {
		const model = await cocoSsd.load({ });
		const prediction = await model.detect(image, 6);
		console.log(prediction)
	}

	return (
		<div>
			{imageData && <img src = {imageData} />}
			<input type="file" ref={searchImage} style={{display: 'none'}} onChange={onSelectImage} />
			<button onClick={openSearchImage}>Select Image</button>
		</div>
	);
}

export default ImageDetector;