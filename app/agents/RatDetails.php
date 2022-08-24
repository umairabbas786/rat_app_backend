<?php

class RatDetails extends ElectroApi {

    const RAT_UID = "rat_uid";

    protected function onAssemble() {
        $this->killWithBadRequestExceptionIfTextualParamIsMissing(self::RAT_UID);
    }

    protected function onDevise() {

        $ratEntity = $this->killFailureIfNullElseGetRatEntity(
            $this->getAppDB()->getRatDao()->getRatWithUid($_POST[self::RAT_UID]),
            null,
            'No Rat found with this Uid'
        );

        /** @var string[] $images */
        $images = json_decode($ratEntity->getGallery() , true);

        $ratImages = [];

        foreach ($images as $image) {
            array_push($ratImages,  /** @_ */
                $this->createLinkForUserAvatarImage($image)
            );
        }

        $this->resSendOK([
            'rat_detail' => [
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
