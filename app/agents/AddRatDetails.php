<?php

use Carbon\Carbon;
use Ramsey\Uuid\Uuid;

class AddRatDetails extends ElectroApi {

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
        if (!isset($_FILES[self::GALLERY])) {
            $this->killAsBadRequestWithMissingParamException(self::GALLERY);
        }
    }

    protected function onDevise() {

        $images = [];

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

            array_push($images, $newName);/** @_ */
        }

        $current_time = Carbon::now();

        $ratEntity = $this->killFailureIfNullElseGetRatEntity(
            $this->getAppDB()->getRatDao()->insertRat(new RatEntity(
                Uuid::uuid4()->toString(),
                $_POST[self::NAME],
                $_POST[self::DOB],
                $_POST[self::DATE_JOINED],
                $_POST[self::GENDER],
                $_POST[self::BREED],
                $_POST[self::COLOR],
                $_POST[self::MEDICAL_HISTORY],
                json_encode($images),
                $current_time,
                $current_time
            )),
            null,
            "Failed to Add Rat Details"
        );

        $ratImages = [];

        foreach ($images as $image) {
            array_push($ratImages,  /** @_ */
                $this->createLinkForUserAvatarImage($image)
            );
        }

        $this->resSendOK([
            'rat' => [
                'uid' => $ratEntity->getUid(),
                'name' => $ratEntity->getName(),
                'date_of_birth' => $ratEntity->getDateOfBirth(),
                'date_joined' => $ratEntity->getDateJoined(),
                'gender' => $ratEntity->getGender(),
                'breed' => $ratEntity->getBreed(),
                'color' => $ratEntity->getColor(),
                'medical_history' => $ratEntity->getMedicalHistory(),
                'gallery' => $ratImages,
                'created_at' => $ratEntity->getCreatedAt()
            ]
        ]);
    }
}
