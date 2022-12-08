#include <string>
#include <vector>
#include <functional>
#include <map>
#include <set>

class IPlayer;
class IActor;
class World;
class Actor;
class Projectile;
class ILocalPlayer;
class IItem;
class AIZoneListener;
class AIZone;
class TimerSet;
class Vector3;
class Rotation;
class Socket;


enum DamageType {PhysicalDamage, FireDamage, ColdDamage, ShockDamage};
enum ItemRarity {ResourceItem, NormalItem, RareItem, LegendaryItem, LeetItem};

template <class T> struct ActorRef {
    T *m_object;

    ActorRef();
    ActorRef(T *);
    ActorRef(const ActorRef<T> &);
    ActorRef<T> & operator=(T *);
    ActorRef<T> & operator=(const ActorRef<T> &);
    T * operator->() const;
    T * Get() const;
    bool operator<(const ActorRef<T> &) const;
};

struct Rotation {
    float pitch;
    float yaw;
    float roll;
  public:
    Rotation(void);
    Rotation(float, float, float);
};
struct QuestStateInfo {
    std::string state;
    uint32_t count;
};

struct Vector3 {
    float x;
    float y;
    float z;
  public:
    Vector3(void);
    Vector3(float, float, float);
    Vector3 operator*(float) const;
    Vector3 & operator*=(float);
    Vector3 operator+(const Vector3 &) const;
    Vector3 & operator+=(const Vector3 &);
    Vector3 operator-(const Vector3 &) const;
    Vector3 & operator-=(const Vector3 &);
    float MagnitudeSquared(void) const;
    float Magnitude(void) const;
    static float DistanceSquared(const Vector3 &, const Vector3 &);
    static float Distance(const Vector3 &, const Vector3 &);
    void Normalize(void);
    static Vector3 Normalize(const Vector3 &);
};

struct ItemCountInfo {
    uint32_t count;
    uint32_t loadedAmmo;
};

struct LocationAndRotation {
    Vector3 location;
    Rotation rotation;
};


class IAchievement {
  public:
    virtual const char * GetName(void);
    virtual const char * GetDisplayName(void);
    virtual const char * GetDescription(void);
};

class AIZone {
  private:
    std::string m_name;
    size_t m_playerCount;
    std::set<AIZoneListener*> m_listeners;

  public:
    AIZone(const std::string &);
    const std::string & GetName(void) const;
    bool IsActive(void) const;
    void OnPlayerEntered(void);
    void OnPlayerLeft(void);
    void AddListener(AIZoneListener *);
    void RemoveListener(AIZoneListener *);
};

class AIZoneListener {
  private:
    AIZone *m_zone;

  public:
    AIZoneListener(void);
    virtual ~AIZoneListener(void);
    void SetAIZone(const std::string &);
    virtual void OnAIZoneActivated(void);
    virtual void OnAIZoneDeactivated(void);
    bool IsAIZoneActive(void);
};

class WriteStream {
  private:
    Socket *m_sock;
    std::vector<unsigned char> m_buffer;

  public:
    WriteStream(Socket *);
    void SetSocket(Socket *);
    void Write8(uint8_t);
    void Write16(uint16_t);
    void Write32(uint32_t);
    void Write64(uint64_t);
    void WriteSaturated16(float);
    void WriteString(const std::string &);
    void WriteFloat(float);
    void WriteVector(const Vector3 &);
    void WriteVector16(const Vector3 &);
    void WriteRotation(const Rotation &);
    void WritePrecisionRotation(const Rotation &);
    void WriteSignedFraction(float);
    void Write(const WriteStream &);
    void Write(const void *, size_t);
    void Flush(void);
    void Clear(void);
};

class Socket {
  protected:
    std::string m_lastErrorMessage;

  public:
    virtual ~Socket(void);
    virtual bool Read(void *, size_t);
    virtual bool Write(const void *, size_t);
    void ReadChecked(void *, size_t);
    uint8_t Read8(void);
    uint16_t Read16(void);
    uint32_t Read32(void);
    uint64_t Read64(void);
    std::string ReadString(void);
    float ReadFloat(void);
    Vector3 ReadVector(void);
    Vector3 ReadVector16(void);
    Rotation ReadRotation(void);
    Rotation ReadPrecisionRotation(void);
    float ReadSignedFraction(void);
    const std::string & GetLastErrorMessage(void) const;
};

class IUE4Actor {
  public:
    virtual void * GetUE4Actor(void);
    virtual void RemoveFromWorld(void);
    virtual Vector3 GetPosition(void);
    virtual Rotation GetRotation(void);
    virtual Vector3 GetProjectilePosition(void);
    virtual Vector3 GetCharacterVelocity(void);
    virtual void SetPosition(const Vector3 &);
    virtual void SetRotation(const Rotation &);
    virtual void SetCharacterVelocity(const Vector3 &);
    virtual void SetForwardAndStrafeMovement(float, float);
    virtual void InterpolatePositionAndRotation(const Vector3 &, const Rotation &, float, float);
    virtual bool MoveToLocation(const Vector3 &);
    virtual bool MoveToRandomLocationInRadius(float);
    virtual bool MoveToActor(IActor *);
    virtual void OnUpdateState(const char *, bool);
    virtual void OnTriggerEvent(const char *, IActor *);
    virtual void OnUpdatePvPEnabled(bool);
    virtual IActor * LineTraceTo(const Vector3 &);
    virtual void FireBullets(IItem *, int32_t, DamageType, const Vector3 &, uint32_t, float);
    virtual void LocalRespawn(const Vector3 &, const Rotation &);
    virtual bool IsOnGround(void);
    virtual void OnReload(uint32_t);
};

class Spawner : public AIZoneListener {
  protected:
    std::vector<ActorRef<Actor>> m_actors;
    Vector3 m_position;
    Rotation m_rotation;
    size_t m_maxActors;
    float m_maxSpawnTimer;
    float m_currentSpawnTimer;

  public:
    Spawner(const std::string &, const Vector3 &, const Rotation &, size_t, float);
    virtual void OnAIZoneActivated(void);
    virtual void OnAIZoneDeactivated(void);
    virtual void Tick(float);
    virtual Actor * Spawn(void);
    void RemoveActor(Actor *);
    virtual size_t GetMaxActors(void);
    virtual float GetSpawnTimer(void);
};

class IQuestState {
  public:
    virtual const char * GetName(void);
    virtual const char * GetDescription(void);
    virtual void CheckForEarlyCompletion(IPlayer *);
    virtual void OnItemAcquired(IPlayer *, IItem *);
    virtual void OnItemPickupUsed(IPlayer *, const char *);
};


class IQuest {
  public:
    virtual const char * GetName(void);
    virtual const char * GetDescription(void);
    virtual IQuestState * GetStartingState(void);
    virtual IQuestState * GetStateByName(const char *);
};





class IActor {
  public:
    virtual ~IActor(void);
    virtual void * GetUE4Actor(void);
    virtual bool IsNPC(void);
    virtual bool IsPlayer(void);
    virtual IPlayer * GetPlayerInterface(void);
    virtual void AddRef(void);
    virtual void Release(void);
    virtual void OnSpawnActor(IUE4Actor *);
    virtual void OnDestroyActor(void);
    virtual const char * GetBlueprintName(void);
    virtual bool IsCharacter(void);
    virtual bool CanBeDamaged(IActor *);
    virtual int32_t GetHealth(void);
    virtual int32_t GetMaxHealth(void);
    virtual void Damage(IActor *, IItem *, int32_t, DamageType);
    virtual void Tick(float);
    virtual bool CanUse(IPlayer *);
    virtual void OnUse(IPlayer *);
    virtual void OnHit(IActor *, const Vector3 &, const Vector3 &);
    virtual void OnAIMoveComplete(void);
    virtual const char * GetDisplayName(void);
    virtual bool IsElite(void);
    virtual bool IsPvPEnabled(void);
    virtual IItem ** GetShopItems(size_t &);
    virtual void FreeShopItems(IItem **);
    virtual int32_t GetBuyPriceForItem(IItem *);
    virtual int32_t GetSellPriceForItem(IItem *);
    virtual Vector3 GetLookPosition(void);
    virtual Rotation GetLookRotation(void);
    virtual IActor * GetOwner(void);
};

class IInventory {
  public:
    virtual ~IInventory(void);
    virtual size_t GetCount(void);
    virtual IItem * GetItem(size_t);
    virtual uint32_t GetItemCount(size_t);
    virtual uint32_t GetItemLoadedAmmo(size_t);
    virtual void Destroy(void);
};

struct PlayerQuestState {
    IQuestState *state;
    uint32_t count;
};

class IFastTravel {
  public:
    virtual ~IFastTravel(void);
    virtual size_t GetCount(void);
    virtual const char * GetRegionName(size_t);
    virtual const char * GetDisplayName(size_t);
    virtual void Destroy(void);
};


class IPlayer {
  public:
    virtual IActor * GetActorInterface(void);
    void AddRef(void);
    void Release(void);
    virtual bool IsLocalPlayer(void) const;
    virtual ILocalPlayer * GetLocalPlayer(void) const;
    virtual const char * GetPlayerName(void);
    virtual const char * GetTeamName(void);
    virtual uint8_t GetAvatarIndex(void);
    virtual const uint32_t * GetColors(void);
    virtual bool IsPvPDesired(void);
    virtual void SetPvPDesired(bool);
    virtual IInventory * GetInventory(void);
    virtual uint32_t GetItemCount(IItem *);
    virtual uint32_t GetLoadedAmmo(IItem *);
    virtual bool AddItem(IItem *, uint32_t, bool);
    virtual bool RemoveItem(IItem *, uint32_t);
    virtual bool AddLoadedAmmo(IItem *, IItem *, uint32_t);
    virtual bool RemoveLoadedAmmo(IItem *, uint32_t);
    virtual IItem * GetItemForSlot(size_t);
    virtual void EquipItem(size_t, IItem *);
    virtual size_t GetCurrentSlot(void);
    virtual void SetCurrentSlot(size_t);
    virtual IItem * GetCurrentItem(void);
    virtual int32_t GetMana(void);
    virtual bool UseMana(int32_t);
    virtual void SetItemCooldown(IItem *, float, bool);
    virtual bool IsItemOnCooldown(IItem *);
    virtual float GetItemCooldown(IItem *);
    virtual bool HasPickedUp(const char *);
    virtual void MarkAsPickedUp(const char *);
    virtual IQuest ** GetQuestList(size_t *);
    virtual void FreeQuestList(IQuest **);
    virtual IQuest * GetCurrentQuest(void);
    virtual void SetCurrentQuest(IQuest *);
    virtual PlayerQuestState GetStateForQuest(IQuest *);
    virtual void StartQuest(IQuest *);
    virtual void AdvanceQuestToState(IQuest *, IQuestState *);
    virtual void CompleteQuest(IQuest *);
    virtual bool IsQuestStarted(IQuest *);
    virtual bool IsQuestCompleted(IQuest *);
    virtual void EnterAIZone(const char *);
    virtual void ExitAIZone(const char *);
    virtual void UpdateCountdown(int32_t);
    void HideCountdown(void);
    virtual bool CanReload(void);
    virtual void RequestReload(void);
    virtual float GetWalkingSpeed(void);
    virtual float GetSprintMultiplier(void);
    virtual float GetJumpSpeed(void);
    virtual float GetJumpHoldTime(void);
    virtual bool CanJump(void);
    virtual void SetJumpState(bool);
    virtual void SetSprintState(bool);
    virtual void SetFireRequestState(bool);
    virtual void TransitionToNPCState(const char *);
    virtual void BuyItem(IActor *, IItem *, uint32_t);
    virtual void SellItem(IActor *, IItem *, uint32_t);
    virtual void EnterRegion(const char *);
    virtual void Respawn(void);
    virtual void Teleport(const char *);
    virtual void Chat(const char *);
    virtual IFastTravel * GetFastTravelDestinations(const char *);
    virtual void FastTravel(const char *, const char *);
    virtual void MarkAsAchieved(IAchievement *);
    virtual bool HasAchieved(IAchievement *);
    virtual void SubmitDLCKey(const char *);
    virtual uint32_t GetCircuitInputs(const char *);
    virtual void SetCircuitInputs(const char *, uint32_t);
    virtual void GetCircuitOutputs(const char *, bool *, size_t);
};

class IItem {
  public:
    virtual ~IItem(void);
    virtual const char * GetName(void);
    virtual const char * GetDisplayName(void);
    virtual const char * GetItemTypeName(void);
    virtual const char * GetDescription(void);
    virtual const char * GetFlavorText(void);
    virtual bool CanEquip(void);
    virtual uint32_t GetMaximumCount(void);
    virtual bool CanActivate(IPlayer *);
    virtual bool CanActivateInInventory(void);
    virtual void Activate(IPlayer *);
    virtual bool ShowInInventory(void);
    virtual bool ShowEventOnPickup(void);
    virtual bool ShowEventOnDuplicatePickup(void);
    virtual bool ShowNotificationOnPickup(void);
    virtual float GetCooldownTime(void);
    virtual ItemRarity GetItemRarity(void);
    virtual IItem * GetAmmoType(void);
    virtual uint32_t GetClipSize(void);
    virtual int32_t GetDamage(void);
    virtual int32_t GetDamagePerSecond(void);
    virtual DamageType GetDamageType(void);
    virtual int32_t GetManaCost(void);
    virtual const char * GetCustomCostDescription(void);
    virtual bool IsAutoFire(void);
    virtual uint32_t GetNumberOfProjectiles(void);
    virtual float GetReloadTime(int32_t);
    virtual bool HasPartialReload(void);
    virtual float GetRange(void);
    virtual int32_t GetTradeValue(void);
    virtual bool IsDynamic(void);
    virtual bool IsUpdating(void);
};

class Actor : public IActor {
  protected:
    size_t m_refs;
    uint32_t m_id;
    IUE4Actor *m_target;
    TimerSet *m_timers;
    std::string m_blueprintName;
    ActorRef<IActor> m_owner;
    int32_t m_health;
    std::map<std::string, bool> m_states;
    float m_forwardMovementFraction;
    float m_strafeMovementFraction;
    Vector3 m_remotePosition;
    Vector3 m_remoteVelocity;
    Rotation m_remoteRotation;
    float m_remoteLocationBlendFactor;
    Spawner *m_spawner;

    virtual void OnKilled(IActor *, IItem *);
    virtual void OnTargetKilled(IActor *, IItem *);
  public:
    Actor(const std::string &);
    virtual ~Actor(void);
    virtual bool IsValid(void) const;
    virtual void * GetUE4Actor(void);
    virtual void AddRef(void);
    virtual void Release(void);
    void RemoveFromWorld(void);
    virtual void OnSpawnActor(IUE4Actor *);
    virtual void OnDestroyActor(void);
    virtual std::string GetDeathMessage(void);
    virtual const char * GetBlueprintName(void);
    virtual bool IsCharacter(void);
    virtual bool IsNPC(void);
    virtual bool IsProjectile(void);
    virtual bool IsPlayer(void);
    virtual IPlayer * GetPlayerInterface(void);
    virtual bool ShouldSendPositionUpdates(void);
    virtual bool ShouldReceivePositionUpdates(void);
    uint32_t GetId(void) const;
    void SetId(uint32_t);
    Vector3 GetPosition(void);
    Vector3 GetProjectilePosition(void);
    virtual Vector3 GetLookPosition(void);
    Rotation GetRotation(void);
    virtual Rotation GetLookRotation(void);
    Vector3 GetVelocity(void);
    float GetForwardMovementFraction(void) const;
    float GetStrafeMovementFraction(void) const;
    bool IsOnGround(void);
    void SetPosition(const Vector3 &);
    void SetRotation(const Rotation &);
    void SetVelocity(const Vector3 &);
    void SetForwardAndStrafeMovement(float, float);
    void SetRemotePositionAndRotation(const Vector3 &, const Rotation &);
    void InterpolateRemotePosition(float);
    virtual IActor * GetOwner(void);
    void LocalRespawn(const Vector3 &, const Rotation &);
    bool MoveToLocation(const Vector3 &);
    bool MoveToRandomLocationInRadius(float);
    bool MoveToActor(IActor *);
    bool GetState(const std::string &);
    virtual void UpdateState(const std::string &, bool);
    virtual void TriggerEvent(const std::string &, IActor *, bool);
    const std::map<std::string, bool> & GetStates(void);
    IActor * LineTraceTo(const Vector3 &);
    void FireBullets(IItem *, int32_t, DamageType, float, uint32_t, float);
    void FireBullets(IItem *, int32_t, DamageType, const Vector3 &, float, uint32_t, float);
    virtual bool CanBeDamaged(IActor *);
    virtual float GetMaximumDamageDistance(void);
    virtual int32_t GetHealth(void);
    virtual int32_t GetMaxHealth(void);
    virtual void Damage(IActor *, IItem *, int32_t, DamageType);
    void PerformSetHealth(int32_t);
    virtual void Tick(float);
    virtual bool CanUse(IPlayer *);
    virtual void OnUse(IPlayer *);
    virtual void PerformUse(IPlayer *);
    virtual void OnHit(IActor *, const Vector3 &, const Vector3 &);
    virtual void OnAIMoveComplete(void);
    virtual const char * GetDisplayName(void);
    virtual bool IsElite(void);
    virtual bool IsPvPEnabled(void);
    virtual IItem ** GetShopItems(size_t &);
    virtual std::vector<IItem*> GetShopItems(void);
    virtual void FreeShopItems(IItem **);
    virtual std::vector<IItem*> GetValidBuyItems(void);
    virtual float GetShopBuyPriceMultiplier(void);
    virtual float GetShopSellPriceMultiplier(void);
    virtual int32_t GetBuyPriceForItem(IItem *);
    virtual int32_t GetSellPriceForItem(IItem *);
    void SetSpawner(Spawner *);
    void AddTimer(const std::string &, float, const std::function<void ()> &);
    void AddTimerWithContext(const std::string &, float, const std::function<void (Actor *)> &);
    void AddRecurringTimer(const std::string &, float, const std::function<void ()> &);
    void AddRecurringTimerWithContext(const std::string &, float, const std::function<void (Actor *)> &);
    void CancelTimer(const std::string &);
    void PerformReloadNotification(uint32_t);
};

enum NPCStateTransitionType {EndConversationTransition, ContinueConversationTransition, ShopTransition};

struct NPCStateTransition {
    std::string text;
    NPCStateTransitionType type;
    std::string nextState;
};

struct NPCState {
    std::string text;
    std::vector<NPCStateTransition> transitions;
};

class NPC : public Actor {
  private:
    std::map<std::string, NPCState> m_states;

  public:
    NPC(const std::string &);
    virtual bool IsNPC(void);
    void AddState(const std::string &, const std::string &);
    void AddStateTransition(const std::string &, const std::string &, const std::string &);
    void AddStateTransitionToEnd(const std::string &, const std::string &);
    void AddStateTransitionToShop(const std::string &, const std::string &);
    std::string GetTextForState(const std::string &);
    std::vector<NPCStateTransition> GetTransitionsForState(const std::string &);
    virtual std::string GetInitialState(IPlayer *);
    virtual void OnTransitionTaken(IPlayer *, const std::string &, const std::string &);
    virtual bool CanUse(IPlayer *);
    virtual void PerformUse(IPlayer *);
    virtual int32_t GetBuyPriceForItem(IItem *);
    virtual int32_t GetSellPriceForItem(IItem *);
};


struct ItemAndCount {
    IItem *item;
    uint32_t count;
    uint32_t loadedAmmo;
};

class Player : public Actor, public IPlayer {
  public:
    uint32_t m_characterId;
    char * m_playerName;
    char * m_teamName;
    uint8_t m_avatarIndex;
    uint32_t m_colors[4];
    std::map<IItem*, ItemAndCount> m_inventory;
    std::set<std::string> m_pickups;
    std::map<IItem*, float> m_cooldowns;
    std::map<std::string, unsigned int> m_circuitInputs;
    std::map<std::string, std::vector<std::allocator<bool>>> m_circuitOutputs;
    bool m_admin;
    bool m_pvpEnabled;
    bool m_pvpDesired;
    float m_pvpChangeTimer;
    int32_t m_pvpChangeReportedTimer;
    bool m_changingServerRegion;
    char * m_currentRegion;
    char * m_changeRegionDestination;
    std::set<std::string> m_aiZones;
    int32_t m_mana;
    float m_manaRegenTimer;
    float m_healthRegenCooldown;
    float m_healthRegenTimer;
    int32_t m_countdown;
    Vector3 m_remoteLookPosition;
    Rotation m_remoteLookRotation;
    IItem *m_equipped[10];
    size_t m_currentSlot;
    std::map<IQuest*, PlayerQuestState> m_questStates;
    IQuest *m_currentQuest;
    float m_walkingSpeed;
    float m_jumpSpeed;
    float m_jumpHoldTime;
    ActorRef<NPC> m_currentNPC;
    std::string m_currentNPCState;
    ILocalPlayer *m_localPlayer;
    WriteStream *m_eventsToSend;
    bool m_itemsUpdated;
    float m_itemSyncTimer;
    uint32_t m_chatMessageCounter;
    float m_chatFloodDecayTimer;
    IItem *m_lastHitByItem;
    float m_lastHitItemTimeLeft;
    float m_circuitStateCooldownTimer;

  protected:
    virtual void OnKilled(IActor *, IItem *);
  public:
    Player(bool);
    virtual ~Player(void);
    virtual bool IsPlayer(void);
    virtual IPlayer * GetPlayerInterface(void);
    virtual IActor * GetActorInterface(void);
    virtual bool CanBeDamaged(IActor *);
    virtual bool IsCharacter(void);
    virtual bool ShouldSendPositionUpdates(void);
    virtual bool ShouldReceivePositionUpdates(void);
    virtual void Tick(float);
    virtual void Damage(IActor *, IItem *, int32_t, DamageType);
    virtual void OnDestroyActor(void);
    void OnKillEvent(IPlayer *, IActor *, IItem *);
    virtual Vector3 GetLookPosition(void);
    virtual Rotation GetLookRotation(void);
    void SetRemoteLookPosition(const Vector3 &);
    void SetRemoteLookRotation(const Rotation &);
    virtual bool CanJump(void);
    virtual bool IsLocalPlayer(void) const;
    virtual ILocalPlayer * GetLocalPlayer(void) const;
    void InitLocalPlayer(ILocalPlayer *);
    bool IsAdmin(void) const;
    void SetPlayerName(const std::string &);
    void SetTeamName(const std::string &);
    void SetAvatarIndex(uint8_t);
    void SetColors(const uint32_t *);
    void SetCharacterId(uint32_t);
    virtual bool IsPvPEnabled(void);
    virtual bool IsPvPDesired(void);
    virtual void SetPvPDesired(bool);
    void PerformSetPvPEnabled(bool);
    void PerformSetPvPDesired(bool);
    void PerformUpdatePvPCountdown(bool, int32_t);
    virtual void UpdateState(const std::string &, bool);
    virtual const char * GetPlayerName(void);
    virtual const char * GetTeamName(void);
    virtual uint8_t GetAvatarIndex(void);
    virtual const uint32_t * GetColors(void);
    uint32_t GetCharacterId(void) const;
    const std::map<IItem*, ItemAndCount> & GetItemList(void) const;
    virtual IInventory * GetInventory(void);
    virtual uint32_t GetItemCount(IItem *);
    virtual uint32_t GetLoadedAmmo(IItem *);
    virtual bool AddItem(IItem *, uint32_t, bool);
    virtual bool RemoveItem(IItem *, uint32_t);
    bool PerformAddItem(IItem *, uint32_t, bool);
    bool PerformRemoveItem(IItem *, uint32_t);
    virtual bool AddLoadedAmmo(IItem *, IItem *, uint32_t);
    virtual bool RemoveLoadedAmmo(IItem *, uint32_t);
    void PerformSetLoadedAmmo(IItem *, uint32_t);
    virtual IItem * GetItemForSlot(size_t);
    virtual void EquipItem(size_t, IItem *);
    void PerformEquipItem(size_t, IItem *);
    virtual size_t GetCurrentSlot(void);
    virtual IItem * GetCurrentItem(void);
    virtual void SetCurrentSlot(size_t);
    void PerformSetCurrentSlot(size_t);
    void SetRemoteItem(IItem *);
    virtual int32_t GetMana(void);
    virtual bool UseMana(int32_t);
    void PerformSetMana(int32_t);
    virtual void SetItemCooldown(IItem *, float, bool);
    virtual bool IsItemOnCooldown(IItem *);
    virtual float GetItemCooldown(IItem *);
    virtual bool HasPickedUp(const char *);
    virtual void MarkAsPickedUp(const char *);
    void PerformMarkAsPickedUp(const std::string &);
    virtual IQuest ** GetQuestList(size_t *);
    virtual void FreeQuestList(IQuest **);
    virtual IQuest * GetCurrentQuest(void);
    virtual PlayerQuestState GetStateForQuest(IQuest *);
    virtual bool IsQuestStarted(IQuest *);
    virtual bool IsQuestCompleted(IQuest *);
    virtual void SetCurrentQuest(IQuest *);
    virtual void StartQuest(IQuest *);
    virtual void AdvanceQuestToState(IQuest *, IQuestState *);
    virtual void CompleteQuest(IQuest *);
    void PerformSetCurrentQuest(IQuest *);
    void PerformStartQuest(IQuest *);
    void PerformAdvanceQuestToState(IQuest *, IQuestState *);
    void PerformCompleteQuest(IQuest *);
    void SetInitialQuestStates(const std::map<std::string, QuestStateInfo> &, const std::string &);
    void SetInitialItemState(const std::map<std::string, ItemCountInfo> &, const std::vector<std::string> &, uint8_t);
    void SetInitialPickupState(const std::set<std::string> &);
    virtual void EnterAIZone(const char *);
    virtual void ExitAIZone(const char *);
    virtual void UpdateCountdown(int32_t);
    void PerformUpdateCountdown(int32_t);
    virtual void TriggerEvent(const std::string &, IActor *, bool);
    virtual bool CanReload(void);
    virtual void RequestReload(void);
    void PerformRequestReload(void);
    virtual float GetWalkingSpeed(void);
    virtual float GetSprintMultiplier(void);
    virtual float GetJumpSpeed(void);
    virtual float GetJumpHoldTime(void);
    virtual void SetJumpState(bool);
    virtual void SetSprintState(bool);
    virtual void SetFireRequestState(bool);
    void SetCurrentNPCState(NPC *, const std::string &);
    void EndNPCConversation(void);
    void EnterNPCShop(NPC *);
    NPC * GetCurrentNPC(void) const;
    const std::string & GetCurrentNPCState(void) const;
    virtual void TransitionToNPCState(const char *);
    void PerformTransitionToNPCState(const std::string &);
    virtual void BuyItem(IActor *, IItem *, uint32_t);
    void PerformBuyItem(IActor *, IItem *, uint32_t);
    virtual void SellItem(IActor *, IItem *, uint32_t);
    void PerformSellItem(IActor *, IItem *, uint32_t);
    virtual void EnterRegion(const char *);
    bool IsChangingRegion(void) const;
    const std::string & GetChangeRegionDestination(void) const;
    void PerformEnterRegion(const std::string &);
    LocationAndRotation GetSpawnLocation(void);
    virtual void Respawn(void);
    void PerformRespawn(void);
    void PerformRespawnAtLocation(const Vector3 &, const Rotation &);
    virtual void Teleport(const char *);
    void PerformTeleport(const std::string &);
    virtual void SendEvent(const WriteStream &);
    virtual void WriteAllEvents(WriteStream &);
    void SyncItems(void);
    virtual void Chat(const char *);
    void PerformChat(const std::string &);
    void ReceiveChat(Player *, const std::string &);
    virtual IFastTravel * GetFastTravelDestinations(const char *);
    virtual void FastTravel(const char *, const char *);
    void PerformFastTravel(const std::string &, const std::string &);
    void OnTravelComplete(const std::string &);
    IItem * GetLastHitByItem(void) const;
    void PerformSetLastHitByItem(IItem *);
    virtual void MarkAsAchieved(IAchievement *);
    virtual bool HasAchieved(IAchievement *);
    virtual void SubmitDLCKey(const char *);
    void PerformSubmitDLCKey(const std::string &);
    virtual uint32_t GetCircuitInputs(const char *);
    virtual void SetCircuitInputs(const char *, uint32_t);
    void PerformSetCircuitInputs(const std::string &, uint32_t);
    virtual void GetCircuitOutputs(const char *, bool *, size_t);
    void PerformSetCircuitOutputs(const std::string &, const std::vector<std::allocator<bool>>);
    void InitCircuitStates(void);
};

class World {
  protected:
    std::set<ActorRef<IPlayer>> m_players;
    std::set<ActorRef<IActor>> m_actors;
    std::map<unsigned int, ActorRef<IActor>> m_actorsById;
    ILocalPlayer *m_localPlayer;
    uint32_t m_nextId;
    std::map<std::string, AIZone*> m_aiZones;

    void AddActorToWorld(Actor *);
    void AddActorToWorldWithId(uint32_t, Actor *);
    void SendEventToAllPlayers(const WriteStream &);
    void SendEventToAllPlayersExcept(Player *, const WriteStream &);
  public:
    World(void);
    virtual ~World(void);
    virtual void Tick(float);
    virtual bool HasLocalPlayer(void);
    ILocalPlayer * GetLocalPlayer(void);
    virtual bool IsAuthority(void);
    virtual void AddLocalPlayer(Player *, ILocalPlayer *);
    virtual void AddRemotePlayer(Player *);
    virtual void AddRemotePlayerWithId(uint32_t, Player *);
    virtual void RemovePlayer(Player *);
    virtual void Use(Player *, Actor *);
    virtual void Activate(Player *, IItem *);
    virtual void Reload(Player *);
    virtual void Jump(bool);
    virtual void Sprint(bool);
    virtual void FireRequest(bool);
    virtual void TransitionToNPCState(Player *, const std::string &);
    virtual void BuyItem(Player *, Actor *, IItem *, uint32_t);
    virtual void SellItem(Player *, Actor *, IItem *, uint32_t);
    virtual void Respawn(Player *);
    virtual void Teleport(Player *, const std::string &);
    virtual void Chat(Player *, const std::string &);
    virtual void FastTravel(Player *, const std::string &, const std::string &);
    virtual void SetPvPDesired(Player *, bool);
    virtual void SubmitDLCKey(Player *, const std::string &);
    virtual void SetCircuitInputs(Player *, const std::string &, uint32_t);
    virtual void SendAddItemEvent(Player *, IItem *, uint32_t);
    virtual void SendRemoveItemEvent(Player *, IItem *, uint32_t);
    virtual void SendLoadedAmmoEvent(Player *, IItem *, uint32_t);
    virtual void SendPickedUpEvent(Player *, const std::string &);
    virtual void EquipItem(Player *, uint8_t, IItem *);
    virtual void SetCurrentSlot(Player *, uint8_t);
    virtual void SendEquipItemEvent(Player *, uint8_t, IItem *);
    virtual void SendCurrentSlotEvent(Player *, uint8_t);
    virtual void SetCurrentQuest(Player *, IQuest *);
    virtual void SendSetCurrentQuestEvent(Player *, IQuest *);
    virtual void SendStartQuestEvent(Player *, IQuest *);
    virtual void SendAdvanceQuestToStateEvent(Player *, IQuest *, IQuestState *);
    virtual void SendCompleteQuestEvent(Player *, IQuest *);
    virtual void SendHealthUpdateEvent(Actor *, int32_t);
    virtual void SendManaUpdateEvent(Player *, int32_t);
    virtual void SendCountdownUpdateEvent(Player *, int32_t);
    virtual void SendPvPCountdownUpdateEvent(Player *, bool, int32_t);
    virtual void SendPvPEnableEvent(Player *, bool);
    virtual void SendStateEvent(Actor *, const std::string &, bool);
    virtual void SendTriggerEvent(Actor *, const std::string &, Actor *, bool);
    virtual void SendFireBulletsEvent(Actor *, IItem *, const Vector3 &, uint32_t, float);
    virtual void SendDisplayEvent(Player *, const std::string &, const std::string &);
    virtual void SendNPCConversationStateEvent(Player *, Actor *, const std::string &);
    virtual void SendNPCConversationEndEvent(Player *);
    virtual void SendNPCShopEvent(Player *, Actor *);
    virtual void SendRespawnEvent(Player *, const Vector3 &, const Rotation &);
    virtual void SendTeleportEvent(Actor *, const Vector3 &, const Rotation &);
    virtual void SendRelativeTeleportEvent(Actor *, const Vector3 &);
    virtual void SendReloadEvent(Player *, IItem *, IItem *, uint32_t);
    virtual void SendPlayerJoinedEvent(Player *);
    virtual void SendPlayerLeftEvent(Player *);
    virtual void SendPlayerItemEvent(Player *);
    virtual void SendActorSpawnEvent(Actor *);
    virtual void SendActorDestroyEvent(Actor *);
    virtual void SendExistingPlayerEvent(Player *, Player *);
    virtual void SendExistingActorEvent(Player *, Actor *);
    virtual void SendChatEvent(Player *, const std::string &);
    virtual void SendKillEvent(Player *, Actor *, IItem *);
    virtual void SendCircuitOutputEvent(Player *, const std::string &, uint32_t, const std::vector<std::allocator<bool>> &);
    virtual void SendActorPositionEvents(Player *);
    virtual void SendRegionChangeEvent(Player *, const std::string &);
    virtual void SendLastHitByItemEvent(Player *, IItem *);
    bool SpawnActor(Actor *, const Vector3 &, const Rotation &);
    bool SpawnActorAtNamedLocation(Actor *, const char *);
    void SpawnActorWithId(uint32_t, Actor *, const Vector3 &, const Rotation &);
    void DestroyActor(Actor *);
    void SendSpawnEventsForExistingActors(Player *);
    void AddAIZone(AIZone *);
    AIZone * GetAIZone(const std::string &);
    void OnPlayerEnteredAIZone(const std::string &);
    void OnPlayerLeftAIZone(const std::string &);
    std::vector<IPlayer*> GetPlayersInRadius(const Vector3 &, float);
    std::vector<Projectile*> GetProjectilesInRadius(const Vector3 &, float);
    Actor * GetActorById(uint32_t);
    void RemoveAllActorsExceptPlayer(Player *);
    void ChangeActorId(Player *, uint32_t);
    bool IsPlayerAlreadyConnected(uint32_t);
};


class ClientWorld : public World {
  public:
    ActorRef<IPlayer> m_activePlayer;
    float m_timeUntilNextNetTick;

  public:
    ClientWorld(void);
    virtual bool HasLocalPlayer(void);
    virtual bool IsAuthority(void);
    virtual void AddLocalPlayer(Player *, ILocalPlayer *);
    virtual void Tick(float);
    virtual void Use(Player *, Actor *);
    virtual void Activate(Player *, IItem *);
    virtual void Reload(Player *);
    virtual void Jump(bool);
    virtual void Sprint(bool);
    virtual void FireRequest(bool);
    virtual void TransitionToNPCState(Player *, const std::string &);
    virtual void BuyItem(Player *, Actor *, IItem *, uint32_t);
    virtual void SellItem(Player *, Actor *, IItem *, uint32_t);
    virtual void Respawn(Player *);
    virtual void Teleport(Player *, const std::string &);
    virtual void Chat(Player *, const std::string &);
    virtual void FastTravel(Player *, const std::string &, const std::string &);
    virtual void SetPvPDesired(Player *, bool);
    virtual void SubmitDLCKey(Player *, const std::string &);
    virtual void SetCircuitInputs(Player *, const std::string &, uint32_t);
    virtual void SendAddItemEvent(Player *, IItem *, uint32_t);
    virtual void SendRemoveItemEvent(Player *, IItem *, uint32_t);
    virtual void SendLoadedAmmoEvent(Player *, IItem *, uint32_t);
    virtual void SendPickedUpEvent(Player *, const std::string &);
    virtual void EquipItem(Player *, uint8_t, IItem *);
    virtual void SetCurrentSlot(Player *, uint8_t);
    virtual void SendEquipItemEvent(Player *, uint8_t, IItem *);
    virtual void SendCurrentSlotEvent(Player *, uint8_t);
    virtual void SetCurrentQuest(Player *, IQuest *);
    virtual void SendSetCurrentQuestEvent(Player *, IQuest *);
    virtual void SendStartQuestEvent(Player *, IQuest *);
    virtual void SendAdvanceQuestToStateEvent(Player *, IQuest *, IQuestState *);
    virtual void SendCompleteQuestEvent(Player *, IQuest *);
    virtual void SendHealthUpdateEvent(Actor *, int32_t);
    virtual void SendManaUpdateEvent(Player *, int32_t);
    virtual void SendCountdownUpdateEvent(Player *, int32_t);
    virtual void SendPvPCountdownUpdateEvent(Player *, bool, int32_t);
    virtual void SendPvPEnableEvent(Player *, bool);
    virtual void SendStateEvent(Actor *, const std::string &, bool);
    virtual void SendTriggerEvent(Actor *, const std::string &, Actor *, bool);
    virtual void SendFireBulletsEvent(Actor *, IItem *, const Vector3 &, uint32_t, float);
    virtual void SendDisplayEvent(Player *, const std::string &, const std::string &);
    virtual void SendNPCConversationStateEvent(Player *, Actor *, const std::string &);
    virtual void SendNPCConversationEndEvent(Player *);
    virtual void SendNPCShopEvent(Player *, Actor *);
    virtual void SendRespawnEvent(Player *, const Vector3 &, const Rotation &);
    virtual void SendTeleportEvent(Actor *, const Vector3 &, const Rotation &);
    virtual void SendRelativeTeleportEvent(Actor *, const Vector3 &);
    virtual void SendReloadEvent(Player *, IItem *, IItem *, uint32_t);
    virtual void SendPlayerJoinedEvent(Player *);
    virtual void SendPlayerLeftEvent(Player *);
    virtual void SendPlayerItemEvent(Player *);
    virtual void SendActorSpawnEvent(Actor *);
    virtual void SendActorDestroyEvent(Actor *);
    virtual void SendExistingPlayerEvent(Player *, Player *);
    virtual void SendExistingActorEvent(Player *, Actor *);
    virtual void SendChatEvent(Player *, const std::string &);
    virtual void SendKillEvent(Player *, Actor *, IItem *);
    virtual void SendCircuitOutputEvent(Player *, const std::string &, uint32_t, const std::vector<std::allocator<bool>> &);
    virtual void SendActorPositionEvents(Player *);
    virtual void SendRegionChangeEvent(Player *, const std::string &);
    virtual void SendLastHitByItemEvent(Player *, IItem *);
};

class TimerSet {
    public:
        struct TimerEvent {
        float timeLeft;
        float initialTime;
        bool recurring;
        bool withContext;
        std::function<void ()> callback;
        std::function<void (Actor *)> contextCallback;
    };

    std::map<std::string, TimerSet::TimerEvent> m_timers;

  public:
    void Add(const std::string &, float, const std::function<void ()> &);
    void AddWithContext(const std::string &, float, const std::function<void (Actor *)> &);
    void AddRecurring(const std::string &, float, const std::function<void ()> &);
    void AddRecurringWithContext(const std::string &, float, const std::function<void (Actor *)> &);
    void Cancel(const std::string &);
    void Clear(void);
    void Tick(Actor *, float);
};





class Projectile : public Actor {
  protected:
    IItem *m_item;
    float m_lifetime;

  public:
    Projectile(IActor *, IItem *, const std::string &);
    virtual bool ShouldSendPositionUpdates(void);
    virtual bool IsProjectile(void);
    virtual int32_t GetDirectDamage(void);
    virtual DamageType GetDamageType(void);
    virtual bool HasSplashDamage(void);
    virtual float GetSplashRadius(void);
    virtual int32_t GetSplashDamage(void);
    virtual bool DamagesOnHit(void);
    IItem * GetItem(void) const;
    virtual void OnHit(IActor *, const Vector3 &, const Vector3 &);
    void DealDamage(IActor *);
    virtual void Tick(float);
    virtual void OnLifetimeEnded(void);
    static bool SpawnProjectile(IActor *, Projectile *);
};

class ILocalPlayer : public IUE4Actor {
  public:
    virtual void SetPlayerInterface(IPlayer *);
    virtual Vector3 GetLookPosition(void);
    virtual Rotation GetLookRotation(void);
    virtual float GetForwardMovementFraction(void);
    virtual float GetStrafeMovementFraction(void);
    virtual void SetCurrentQuest(IQuest *, IQuestState *, uint32_t);
    virtual void DisplayMessage(const char *, const char *);
    virtual void DisplayEvent(const char *, const char *);
    virtual void OnEquip(size_t, IItem *);
    virtual void OnChangeSlot(size_t);
    virtual void OnUpdateCountdown(int32_t);
    virtual void OnUpdatePvPCountdown(bool, int32_t);
    virtual void OnNewItem(const char *, uint32_t);
    virtual void OnNPCConversationState(IActor *, const char *, const char **, const char **, size_t);
    virtual void OnNPCConversationEnd(void);
    virtual void OnNPCShop(IActor *);
    virtual void OnChatMessage(const char *, bool, const char *);
    virtual void OnPlayerKillMessage(const char *, bool, const char *, bool, IItem *);
    virtual void OnPlayerSuicideMessage(const char *, bool, IItem *);
    virtual void OnPlayerDeadMessage(const char *, bool, const char *);
    virtual void OnAchievement(const char *);
    virtual void OnLocalDeath(IActor *, IItem *);
};