<?php

class ShowAllRats extends ElectroApi {

    protected function onDevise() {

        /** @var RatEntity[] $ratEntities */
        $ratEntities = $this->getAppDB()->getRatDao()->getAllRat();

        $ratMeta = [];
        foreach ($ratEntities as $ratEntity) {

            $images = json_decode($ratEntity->getGallery());

            $ratImages = [];

            foreach ($images as $image) {
                array_push($ratImages,  /** @_ */
                    $this->createLinkForUserAvatarImage($image)
                );
            }

            array_push($ratMeta , /** @_ */ [
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
            ]);
        }
        $this->resSendOK([
            'all_rats' => $ratMeta
        ]);
    }
}
