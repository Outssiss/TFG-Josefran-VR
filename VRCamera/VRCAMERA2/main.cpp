#include "vrCamera.h"
#include <windows.h>

void SaveImageToFile(const std::vector<uint8_t>& imageData, int width, int height, const std::string& filename) {
    cv::Mat frame(height, width, CV_8UC4, (void*)imageData.data());

    // OpenCV uses BGR order, so we need to convert RGBA to BGR
    cv::cvtColor(frame, frame, cv::COLOR_RGBA2BGR);

    // Save the image using OpenCV
    cv::imwrite(filename, frame);
}

void DisplayImage(const std::vector<uint8_t>& imageData, int width, int height) {
    cv::Mat frame(height, width, CV_8UC4, (void*)imageData.data());

    // OpenCV uses BGR order, so we need to convert RGBA to BGR
    cv::cvtColor(frame, frame, cv::COLOR_RGBA2BGR);

    // Display the image in an OpenCV window
    cv::imshow("Tracked Camera", frame);
    cv::waitKey(1); // Add a short delay to allow OpenCV to handle events
}

int main(int argc, char* argv[]) {

    m_pVRSystem = nullptr;
    m_pVRTrackedCamera = nullptr;

    m_hTrackedCamera = INVALID_TRACKED_CAMERA_HANDLE;

    m_nCameraFrameWidth = 0;
    m_nCameraFrameHeight = 0;
    m_nCameraFrameBufferSize = 0;
    m_pCameraFrameBuffer = nullptr;

    vr::EVRInitError eError = vr::VRInitError_None;
    m_pVRSystem = vr::VR_Init(&eError, vr::VRApplication_Scene);
    if (eError != vr::VRInitError_None)
    {
        m_pVRSystem = nullptr;
        char buf[1024];
        sprintf_s(buf, sizeof(buf), "Unable to init VR runtime: %s", vr::VR_GetVRInitErrorAsSymbol(eError));
        std::printf("%s\n", buf);
        return false;
    }
    else
    {
        char systemName[1024];
        char serialNumber[1024];
        m_pVRSystem->GetStringTrackedDeviceProperty(vr::k_unTrackedDeviceIndex_Hmd, vr::Prop_TrackingSystemName_String, systemName, sizeof(systemName));
        m_pVRSystem->GetStringTrackedDeviceProperty(vr::k_unTrackedDeviceIndex_Hmd, vr::Prop_SerialNumber_String, serialNumber, sizeof(serialNumber));

        m_HMDSerialNumberString = serialNumber;

        std::printf("VR HMD: %s %s\n", systemName, serialNumber);
    }

    m_pVRTrackedCamera = vr::VRTrackedCamera();

    if (!m_pVRTrackedCamera)
    {
        std::printf("Unable to get Tracked Camera interface.\n");
        return false;
    }

    bool bHasCamera = false;
    vr::EVRTrackedCameraError nCameraError = m_pVRTrackedCamera->HasCamera(vr::k_unTrackedDeviceIndex_Hmd, &bHasCamera);

    if (nCameraError != vr::VRTrackedCameraError_None || !bHasCamera)
    {
        std::printf("No Tracked Camera Available! (%s)\n", m_pVRTrackedCamera->GetCameraErrorNameFromEnum(nCameraError));
        return false;
    }

    vr::ETrackedPropertyError propertyError;
    char buffer[128];
    m_pVRSystem->GetStringTrackedDeviceProperty(vr::k_unTrackedDeviceIndex_Hmd, vr::Prop_CameraFirmwareDescription_String, buffer, sizeof(buffer), &propertyError);

    if (propertyError != vr::TrackedProp_Success)
    {
        std::printf("Failed to get tracked camera firmware description!\n");
        return false;
    }

    std::printf("Camera Firmware: %s\n\n", buffer);

    std::printf("StartVideoPreview()\n");

    uint32_t nCameraFrameBufferSize = 0;

    if (m_pVRTrackedCamera->GetCameraFrameSize(vr::k_unTrackedDeviceIndex_Hmd, vr::VRTrackedCameraFrameType_Undistorted, &m_nCameraFrameWidth, &m_nCameraFrameHeight, &nCameraFrameBufferSize) != vr::VRTrackedCameraError_None)
    {
        std::printf("GetCameraFrameBounds() Failed!\n");
        return false;
    }

    if (nCameraFrameBufferSize && nCameraFrameBufferSize != m_nCameraFrameBufferSize)
    {
        delete[] m_pCameraFrameBuffer;
        m_nCameraFrameBufferSize = nCameraFrameBufferSize;
        m_pCameraFrameBuffer = new uint8_t[m_nCameraFrameBufferSize];
        memset(m_pCameraFrameBuffer, 0, m_nCameraFrameBufferSize);
    }

    m_nLastFrameSequence = 0;
    
    m_pVRTrackedCamera->AcquireVideoStreamingService(vr::k_unTrackedDeviceIndex_Hmd, &m_hTrackedCamera);
    if (m_hTrackedCamera == INVALID_TRACKED_CAMERA_HANDLE)
    {
        std::printf("AcquireVideoStreamingService() Failed!\n");
        return false;
    }

    while (true) {
        vr::CameraVideoStreamFrameHeader_t videoFrame;
        std::vector<uint8_t> imageData(m_nCameraFrameBufferSize);
        vr::EVRTrackedCameraError frameError = m_pVRTrackedCamera->GetVideoStreamFrameBuffer(m_hTrackedCamera, vr::VRTrackedCameraFrameType_Distorted, imageData.data(), m_nCameraFrameBufferSize, &videoFrame, sizeof(videoFrame));
        
        //SaveImageToFile(imageData, videoFrame.nWidth, videoFrame.nHeight, "camera_image.png");
        //std::printf("Saved image i think");

        DisplayImage(imageData, videoFrame.nWidth, videoFrame.nHeight);
    }

	return 0;
}