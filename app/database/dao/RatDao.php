<?php

class RatDao extends TableDao {


    public function __construct(mysqli $connection) { // <***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
        parent::__construct($connection);
    } // </***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>

    public function insertRat(RatEntity $ratEntity): ?RatEntity { // <***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
        $query = QueryBuilder::withQueryType(QueryType::INSERT)
            ->withTableName(RatEntity::TABLE_NAME)
            ->columns([
                RatTableSchema::UID,
                RatTableSchema::NAME,
                RatTableSchema::DATE_OF_BIRTH,
                RatTableSchema::DATE_JOINED,
                RatTableSchema::GENDER,
                RatTableSchema::BREED,
                RatTableSchema::COLOR,
                RatTableSchema::MEDICAL_HISTORY,
                RatTableSchema::GALLERY,
                RatTableSchema::CREATED_AT,
                RatTableSchema::UPDATED_AT
            ])
            ->values([
                $this->escape_string($ratEntity->getUid()),
                $this->escape_string($ratEntity->getName()),
                $this->escape_string($ratEntity->getDateOfBirth()),
                $this->escape_string($ratEntity->getDateJoined()),
                $this->escape_string($ratEntity->getGender()),
                $this->escape_string($ratEntity->getBreed()),
                $this->escape_string($ratEntity->getColor()),
                $this->escape_string($ratEntity->getMedicalHistory()),
                $this->escape_string($ratEntity->getGallery()),
                $this->escape_string($ratEntity->getCreatedAt()),
                $this->escape_string($ratEntity->getUpdatedAt())
            ])
            ->generate();

        $result = mysqli_query($this->getConnection(), $query);

        if ($result) {
            return $this->getRatWithId($this->inserted_id());
        }
        return null;
    } // </***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>

    public function getRatWithId(string $id): ?RatEntity { // <***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
        $query = QueryBuilder::withQueryType(QueryType::SELECT)
             ->withTableName(RatEntity::TABLE_NAME)
             ->columns(['*'])
             ->whereParams([
                [RatTableSchema::ID, '=', $this->escape_string($id)]
             ])
             ->generate();

        $result = mysqli_query($this->getConnection(), $query);

        if ($result && $result->num_rows >= 1) {
            return RatFactory::mapFromDatabaseResult(mysqli_fetch_assoc($result));
        }
        return null;
    } // </***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>

    public function getRatWithUid(string $uid): ?RatEntity { // <***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
        $query = QueryBuilder::withQueryType(QueryType::SELECT)
             ->withTableName(RatEntity::TABLE_NAME)
             ->columns(['*'])
             ->whereParams([
                [RatTableSchema::UID, '=', $this->escape_string($uid)]
             ])
             ->generate();

        $result = mysqli_query($this->getConnection(), $query);

        if ($result && $result->num_rows >= 1) {
            return RatFactory::mapFromDatabaseResult(mysqli_fetch_assoc($result));
        }
        return null;
    } // </***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>

    public function getAllRat(): array { // <***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
        $query = QueryBuilder::withQueryType(QueryType::SELECT)
             ->withTableName(RatEntity::TABLE_NAME)
             ->columns(['*'])
             ->generate();

        $result = mysqli_query($this->getConnection(), $query);

        $rats = [];

        if ($result) {
            while($row = mysqli_fetch_assoc($result)) {
                array_push($rats, RatFactory::mapFromDatabaseResult($row));
            }
        }
        return $rats;
    } // </***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>

    public function updateRat(RatEntity $ratEntity): ?RatEntity { // <***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
        $query = QueryBuilder::withQueryType(QueryType::UPDATE)
            ->withTableName(RatEntity::TABLE_NAME)
            ->updateParams([
                [RatTableSchema::NAME, $this->escape_string($ratEntity->getName())],
                [RatTableSchema::DATE_OF_BIRTH, $this->escape_string($ratEntity->getDateOfBirth())],
                [RatTableSchema::DATE_JOINED, $this->escape_string($ratEntity->getDateJoined())],
                [RatTableSchema::GENDER, $this->escape_string($ratEntity->getGender())],
                [RatTableSchema::BREED, $this->escape_string($ratEntity->getBreed())],
                [RatTableSchema::COLOR, $this->escape_string($ratEntity->getColor())],
                [RatTableSchema::MEDICAL_HISTORY, $this->escape_string($ratEntity->getMedicalHistory())],
                [RatTableSchema::GALLERY, $this->escape_string($ratEntity->getGallery())],
                [RatTableSchema::CREATED_AT, $this->escape_string($ratEntity->getCreatedAt())],
                [RatTableSchema::UPDATED_AT, $this->escape_string($ratEntity->getUpdatedAt())]
            ])
            ->whereParams([
                [RatTableSchema::ID, '=', $this->escape_string($ratEntity->getId())]
            ])
            ->generate();

        $result = mysqli_query($this->getConnection(), $query);

        if ($result) {
            return $this->getRatWithId($ratEntity->getId());
        }
        return null;
    } // </***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>

    public function deleteRat(RatEntity $ratEntity) { // <***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
        $query = QueryBuilder::withQueryType(QueryType::DELETE)
            ->withTableName(RatEntity::TABLE_NAME)
            ->whereParams([
                [RatTableSchema::ID, '=', $this->escape_string($ratEntity->getId())]
            ])
            ->generate();

        while(true) {
            if (mysqli_query($this->getConnection(), $query)) {
                break;
            }
        }
    } // </***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>

    public function deleteAllRats() { // <***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>
        $query = QueryBuilder::withQueryType(QueryType::DELETE)
            ->withTableName(RatEntity::TABLE_NAME)
            ->generate();

        while(true) {
            if (mysqli_query($this->getConnection(), $query)) {
                break;
            }
        }
    } // </***_ELECTRO_GENERATED_DO_NOT_REMOVE_***>

}
