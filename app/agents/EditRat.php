<?php

use Carbon\Carbon;

class EditRat extends ElectroApi {

    const RAT_UID = "rat_uid";
    const NAME = "name";
    const DOB = "date_of_birth";
    const DATE_JOINED = "date_joined";
    const GENDER = "gender";
    const BREED = "breed";
    const COLOR = "color";
    const MEDICAL_HISTORY = "medical_history";
    const GALLERY = "gallery";

    protected function onAssemble() {
        foreach ([self::NAME,self::DOB,self::DATE_JOINED,self::GENDER,self::BREED,self::COLOR,self::MEDICAL_HISTORY] as $item) {
            $this->killWithBadRequestExceptionIfTextualParamIsMissing($item);
        }
    }

    protected function onDevise() {

        $ratEntity = $this->killFailureIfNullElseGetRatEntity(
            $this->getAppDB()->getRatDao()->getRatWithUid($_POST[self::RAT_UID]),
            null,
            'No Rat found with this Uid'
        );

        $images = [];

        if(isset($_FILES[self::GALLERY])) {

            if (count($_FILES[self::GALLERY]['tmp_name']) > 7) {
                $this->killFailureWithMsg('Images count should be less then 7');
            }

            for ($i = 0; $i < count($_FILES[self::GALLERY]['tmp_name']); $i++) {
                // get file path info
                $fileInfo = pathinfo($_FILES[self::GALLERY]['name'][$i]);
                // split file name with '.'
                $tmp = explode(".", $_FILES[self::GALLERY]['name'][$i]);
                // generate a new random name for image
                $newName = time() . rand(0, 99999) . "." . end($tmp);
                // move file to directory  to save

                if (!file_exists($this->getUserAvatarImageDirPath())) {
                    mkdir($this->getUserAvatarImageDirPath(), 0777, true);
                }

                if (!move_uploaded_file($_FILES[self::GALLERY]['tmp_name'][$i], $this->getUserAvatarImageDirPath() . '/' . $newName)) {
                    $this->killFailureWithMsg('failed_to_save_images');
                }

                array_push($images, $newName);
                /** @_ */
            }
            $ratEntity->setGallery(json_encode($images));
        }

        $current_time = Carbon::now();

        $ratEntity->setName($_POST[self::NAME]);
        $ratEntity->setDateOfBirth($_POST[self::DOB]);
        $ratEntity->setDateJoined($_POST[self::DATE_JOINED]);
        $ratEntity->setGender($_POST[self::GENDER]);
        $ratEntity->setBreed($_POST[self::BREED]);
        $ratEntity->setColor($_POST[self::COLOR]);
        $ratEntity->setMedicalHistory($_POST[self::MEDICAL_HISTORY]);
        $ratEntity->setUpdatedAt($current_time);

        $ratEntity = $this->killFailureIfNullElseGetRatEntity(
            $this->getAppDB()->getRatDao()->updateRat($ratEntity)
            , null
            , 'Failed to update Rat'
        );

        $this->resSendOK([
            'rat_updated' => true
        ]);
    }
}
