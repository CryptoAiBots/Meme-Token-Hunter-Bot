const { expect } = require("chai")

const config = require("../config.json")

describe("MemeHunter", () => {
  let owner
  let MemeHunter

  beforeEach(async () => {
    [owner] = await ethers.getSigners()

    MemeHunter = await hre.ethers.deployContract(
      "MemeHunter",
      [
        config.SUSHISWAP.V2_ROUTER_02_ADDRESS,
        config.UNISWAP.V2_ROUTER_02_ADDRESS
      ]
    )

    await MemeHunter.waitForDeployment()
  })

  describe("Deployment", () => {
    it("Sets the sRouter", async () => {
      expect(await MemeHunter.sRouter()).to.equal(config.SUSHISWAP.V2_ROUTER_02_ADDRESS)
    })

    it("Sets the uRouter", async () => {
      expect(await MemeHunter.uRouter()).to.equal(config.UNISWAP.V2_ROUTER_02_ADDRESS)
    })

    it("Sets the owner", async () => {
      expect(await MemeHunter.owner()).to.equal(await owner.getAddress())
    })
  })

  describe("Trading", () => {

    /**
     * Feel Free to customize and add in your own unit testing here.
     */

  })
})                  