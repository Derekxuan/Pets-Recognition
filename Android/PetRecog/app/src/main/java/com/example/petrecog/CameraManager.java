package com.example.petrecog;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;

import java.util.Stack;

public class CameraManager {

    private static CameraManager mInstance;
    private Stack<Activity> cameras = new Stack<Activity>();

    public static CameraManager getInst() {
        if (mInstance == null) {
            synchronized (CameraManager.class) {
                if (mInstance == null)
                    mInstance = new CameraManager();
            }
        }
        return mInstance;
    }

    //打开照相界面
    public void openCamera(Context context) {
        Intent intent = new Intent(context, CameraActivity.class);
        context.startActivity(intent);
    }

    //判断图片是否需要裁剪
//    public void processPhotoItem(Activity activity, PhotoItem photo) {
//        Uri uri = photo.getImageUri().startsWith("file:") ? Uri.parse(photo
//                .getImageUri()) : Uri.parse("file://" + photo.getImageUri());
//        if (ImageUtils.isSquare(photo.getImageUri())) {
//            Intent newIntent = new Intent(activity, PhotoProcessActivity.class);
//            newIntent.setData(uri);
//            activity.startActivity(newIntent);
//        } else {
//            Intent i = new Intent(activity, CropPhotoActivity.class);
//            i.setData(uri);
//            //TODO稍后添加
//            activity.startActivityForResult(i, AppConstants.REQUEST_CROP);
//        }
//    }

    public void close() {
        for (Activity act : cameras) {
            try {
                act.finish();
            } catch (Exception e) {

            }
        }
        cameras.clear();
    }

}
