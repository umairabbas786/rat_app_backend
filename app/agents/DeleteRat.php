<?php

class DeleteRat extends ElectroApi {

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

        $this->getAppDB()->getRatDao()->deleteRat($ratEntity);

        $this->resSendOK([
            'rat_deleted_successfully' => true
        ]);
    }
}
