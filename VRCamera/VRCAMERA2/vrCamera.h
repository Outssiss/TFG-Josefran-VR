#include "openvr.h"
#include <string>
#include <iostream>
#include <print>
#include <opencv2/opencv.hpp>

vr::IVRSystem* m_pVRSystem;
vr::IVRTrackedCamera* m_pVRTrackedCamera;

vr::TrackedCameraHandle_t	m_hTrackedCamera;

uint32_t				m_nCameraFrameWidth;
uint32_t				m_nCameraFrameHeight;
uint32_t				m_nCameraFrameBufferSize;
uint8_t* m_pCameraFrameBuffer;

uint32_t				m_nLastFrameSequence;

std::string m_HMDSerialNumberString;